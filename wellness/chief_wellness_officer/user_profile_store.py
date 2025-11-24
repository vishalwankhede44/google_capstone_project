"""
Centralized user profile management for the Chief Wellness Officer.
Stores and retrieves user demographic and fitness information across sessions.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import json
import os
import threading


@dataclass
class UserProfile:
    """Complete user profile with demographic and fitness information."""
    user_id: str
    age: Optional[int] = None
    weight: Optional[float] = None  # in kg
    gender: Optional[str] = None
    height: Optional[float] = None  # in cm
    fitness_level: Optional[str] = None  # beginner, intermediate, advanced
    injuries: Optional[str] = None
    goals: Optional[str] = None
    
    def is_complete_for_exercise(self) -> bool:
        """Check if profile has all required fields for exercise planning."""
        return all([
            self.age is not None,
            self.weight is not None,
            self.gender is not None,
            self.fitness_level is not None
        ])
    
    def missing_fields_for_exercise(self) -> list[str]:
        """Return list of missing fields needed for exercise planning."""
        missing = []
        if self.age is None:
            missing.append("age")
        if self.weight is None:
            missing.append("weight (in kg)")
        if self.gender is None:
            missing.append("gender")
        if self.fitness_level is None:
            missing.append("fitness level (beginner/intermediate/advanced)")
        return missing
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


class UserProfileStore:
    """Thread-safe persistent store for user profiles."""
    
    def __init__(self, storage_path: str = "data/user_profiles.json"):
        self._lock = threading.Lock()
        self._storage_path = storage_path
        self._profiles: Dict[str, UserProfile] = {}
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        """Load profiles from disk if file exists."""
        if os.path.exists(self._storage_path):
            try:
                with open(self._storage_path, 'r') as f:
                    data = json.load(f)
                    for user_id, profile_data in data.items():
                        self._profiles[user_id] = UserProfile(**profile_data)
            except Exception as e:
                print(f"Warning: Could not load user profiles: {e}")
    
    def _save_to_disk(self) -> None:
        """Persist profiles to disk."""
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        try:
            data = {
                user_id: profile.to_dict()
                for user_id, profile in self._profiles.items()
            }
            with open(self._storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save user profiles: {e}")
    
    def get_profile(self, user_id: str) -> UserProfile:
        """Get user profile, creating a new one if it doesn't exist."""
        with self._lock:
            if user_id not in self._profiles:
                self._profiles[user_id] = UserProfile(user_id=user_id)
            return self._profiles[user_id]
    
    def update_profile(self, user_id: str, **updates) -> UserProfile:
        """Update user profile with new information."""
        # Avoid nested locking by operating directly on the internal dict
        with self._lock:
            if user_id not in self._profiles:
                self._profiles[user_id] = UserProfile(user_id=user_id)
            profile = self._profiles[user_id]

            # Update only provided fields
            for key, value in updates.items():
                if hasattr(profile, key) and value is not None:
                    setattr(profile, key, value)

            # Persist and return updated profile
            self._profiles[user_id] = profile
            self._save_to_disk()
            return profile


# Global instance
profile_store = UserProfileStore()
