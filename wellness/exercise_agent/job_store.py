from dataclasses import dataclass
from typing import Dict, Any, Optional
import threading


def _default_params() -> Dict[str, Any]:
    return {}


@dataclass
class PendingJob:
    ticket_id: str
    invocation_id: str
    function_call_id: str
    user_id: str
    session_id: str
    params: Dict[str, Any]


class InMemoryJobStore:
    """Thread-safe in-memory store for long running tool jobs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._jobs: Dict[str, PendingJob] = {}

    def add(self, job: PendingJob) -> None:
        with self._lock:
            self._jobs[job.ticket_id] = job

    def pop(self, ticket_id: str) -> Optional[PendingJob]:
        with self._lock:
            return self._jobs.pop(ticket_id, None)

    def get(self, ticket_id: str) -> Optional[PendingJob]:
        with self._lock:
            return self._jobs.get(ticket_id)


job_store = InMemoryJobStore()
