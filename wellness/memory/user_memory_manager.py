"""User memory manager for storing long-term preferences and past plans.

The manager persists lightweight summaries per user so the Chief Wellness
Officer can tailor recommendations when users return. It also applies a
simple compaction strategy that collapses older entries into
chronological summaries and caps the total entries retained per user.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class MemoryEntry:
    """A single stored memory fragment."""

    summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, str] | None = None


class UserMemoryManager:
    """File-backed memory store with basic compaction policies."""

    def __init__(self, storage_path: str = "data/user_memory.json", max_entries: int = 5) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.max_entries = max_entries
        self._lock = threading.Lock()
        if not self.storage_path.exists():
            self._write({})

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_user_memories(self, user_id: str) -> List[MemoryEntry]:
        data = self._read()
        raw_entries = data.get(user_id, [])
        return [MemoryEntry(**entry) for entry in raw_entries]

    def add_memory(self, user_id: str, summary: str, metadata: Dict[str, str] | None = None) -> MemoryEntry:
        entry = MemoryEntry(summary=summary, metadata=metadata)
        with self._lock:
            data = self._read()
            entries = data.get(user_id, [])
            entries.append(entry.__dict__)
            entries = self._compact_entries(entries)
            data[user_id] = entries
            self._write(data)
        return entry

    # ------------------------------------------------------------------
    # Compaction strategies
    # ------------------------------------------------------------------
    def _compact_entries(self, entries: List[Dict]) -> List[Dict]:
        if len(entries) <= self.max_entries:
            return entries

        # Summarize everything older than the newest window into a single entry
        stale = entries[: -self.max_entries]
        recent = entries[-self.max_entries :]
        summary_text = " | ".join(item.get("summary", "") for item in stale if item.get("summary"))
        compounded = MemoryEntry(
            summary=f"Historical preferences: {summary_text}",
            metadata={"compacted": "true"},
        )
        return [compounded.__dict__, *recent]

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _read(self) -> Dict[str, List[Dict]]:
        if not self.storage_path.exists():
            return {}
        try:
            return json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write(self, data: Dict[str, List[Dict]]) -> None:
        self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# Shared singleton instance used across the app
memory_manager = UserMemoryManager()
