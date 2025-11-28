"""
Tools for the Chief Wellness Officer to manage user profiles.
These tools enable HITL (Human-In-The-Loop) at the orchestrator level.
"""

from typing import Dict, Any, Optional

from google.adk.tools.tool_context import ToolContext
from .user_profile_store import profile_store, UserProfile


def get_user_profile(tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Retrieve the current user's profile.
    Use this at the start of every conversation to check what information you already have.
    
    Returns:
        Dictionary containing the user's profile and completion status
    """
    if tool_context is None:
        return {"error": "No tool context available"}
    
    user_id = tool_context.user_id
    profile = profile_store.get_profile(user_id)
    
    return {
        "user_id": user_id,
        "profile": profile.to_dict(),
        "is_complete_for_exercise": profile.is_complete_for_exercise(),
        "missing_for_exercise": profile.missing_fields_for_exercise(),
        "is_complete_for_nutrition": profile.is_complete_for_nutrition(),
        "missing_for_nutrition": profile.missing_fields_for_nutrition()
    }


def update_user_profile(
    age: Optional[int] = None,
    weight: Optional[float] = None,
    gender: Optional[str] = None,
    height: Optional[float] = None,
    fitness_level: Optional[str] = None,
    injuries: Optional[str] = None,
    goals: Optional[str] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Update the user's profile with new information.
    Call this whenever the user provides demographic or fitness information.
    
    Args:
        age: User's age in years
        weight: User's weight in kg
        gender: User's gender (male, female, other)
        height: User's height in cm
        fitness_level: beginner, intermediate, or advanced
        injuries: Any injuries or physical limitations
        goals: User's wellness goals
        
    Returns:
        Updated profile with completion status
    """
    if tool_context is None:
        return {"error": "No tool context available"}
    
    user_id = tool_context.user_id
    profile = profile_store.update_profile(
        user_id=user_id,
        age=age,
        weight=weight,
        gender=gender,
        height=height,
        fitness_level=fitness_level,
        injuries=injuries,
        goals=goals
    )
    
    return {
        "user_id": user_id,
        "profile": profile.to_dict(),
        "is_complete_for_exercise": profile.is_complete_for_exercise(),
        "missing_for_exercise": profile.missing_fields_for_exercise(),
        "is_complete_for_nutrition": profile.is_complete_for_nutrition(),
        "missing_for_nutrition": profile.missing_fields_for_nutrition(),
        "message": "Profile updated successfully"
    }
