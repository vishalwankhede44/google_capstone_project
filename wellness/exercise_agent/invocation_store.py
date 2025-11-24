"""
Persistent store for tracking incomplete tool invocations across sessions.
Enables true HITL (Human-In-The-Loop) where users can provide missing parameters
in future sessions and the agent resumes from where it left off.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import threading
import json
import os


@dataclass
class PartialInvocation:
    """Represents an incomplete tool invocation waiting for user input."""
    invocation_id: str
    user_id: str
    tool_name: str
    collected_params: Dict[str, Any] = field(default_factory=dict)
    missing_params: List[str] = field(default_factory=list)
    timestamp: str = ""


class InvocationStore:
    """Thread-safe persistent store for partial tool invocations."""

    def __init__(self, storage_path: str = "data/invocations.json"):
        self._lock = threading.Lock()
        self._storage_path = storage_path
        self._invocations: Dict[str, PartialInvocation] = {}
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Load invocations from disk if file exists."""
        if os.path.exists(self._storage_path):
            try:
                with open(self._storage_path, 'r') as f:
                    data = json.load(f)
                    for inv_id, inv_data in data.items():
                        self._invocations[inv_id] = PartialInvocation(**inv_data)
            except Exception as e:
                print(f"Warning: Could not load invocations from disk: {e}")

    def _save_to_disk(self) -> None:
        """Persist invocations to disk."""
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        try:
            data = {
                inv_id: {
                    "invocation_id": inv.invocation_id,
                    "user_id": inv.user_id,
                    "tool_name": inv.tool_name,
                    "collected_params": inv.collected_params,
                    "missing_params": inv.missing_params,
                    "timestamp": inv.timestamp,
                }
                for inv_id, inv in self._invocations.items()
            }
            with open(self._storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save invocations to disk: {e}")

    def save_partial(self, invocation: PartialInvocation) -> None:
        """Save a partial invocation."""
        with self._lock:
            self._invocations[invocation.invocation_id] = invocation
            self._save_to_disk()

    def get_by_user(self, user_id: str) -> Optional[PartialInvocation]:
        """Get the most recent pending invocation for a user."""
        with self._lock:
            user_invocations = [
                inv for inv in self._invocations.values()
                if inv.user_id == user_id
            ]
            if user_invocations:
                # Return most recent (last in list)
                return user_invocations[-1]
            return None

    def get_by_id(self, invocation_id: str) -> Optional[PartialInvocation]:
        """Get a specific invocation by ID."""
        with self._lock:
            return self._invocations.get(invocation_id)

    def complete(self, invocation_id: str) -> None:
        """Remove a completed invocation."""
        with self._lock:
            if invocation_id in self._invocations:
                del self._invocations[invocation_id]
                self._save_to_disk()

    def clear_user_invocations(self, user_id: str) -> None:
        """Clear all pending invocations for a user."""
        with self._lock:
            self._invocations = {
                inv_id: inv
                for inv_id, inv in self._invocations.items()
                if inv.user_id != user_id
            }
            self._save_to_disk()


# Global instance
invocation_store = InvocationStore()
