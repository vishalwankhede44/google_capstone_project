"""Tools that allow the CWO to read/write long-term user memories."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory.user_memory_manager import MemoryEntry, memory_manager


def _entry_to_dict(entry: MemoryEntry) -> Dict[str, Any]:
    return {
        "summary": entry.summary,
        "timestamp": entry.timestamp,
        "metadata": entry.metadata or {},
    }


def load_user_memories(user_id: str) -> Dict[str, Any]:
    """Return stored memories for the given user_id."""
    entries = memory_manager.get_user_memories(user_id)
    return {
        "user_id": user_id,
        "count": len(entries),
        "memories": [_entry_to_dict(entry) for entry in entries],
    }


def remember_user_insight(
    user_id: str,
    summary: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Persist a new memory summary for the given user_id."""
    entry = memory_manager.add_memory(user_id=user_id, summary=summary, metadata=metadata)
    return {
        "user_id": user_id,
        "status": "stored",
        "memory": _entry_to_dict(entry),
    }
