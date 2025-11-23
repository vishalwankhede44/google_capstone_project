import uuid
from typing import Dict

from google.adk.tools.tool_context import ToolContext

from .job_store import PendingJob, job_store


def build_workout_plan(
    goal: str,
    minutes_per_day: int,
    days_per_week: int,
    fitness_level: str,
    injuries: str = "none",
) -> Dict:
    """Deterministically builds the workout plan payload."""

    goal = goal.lower()
    fitness_level = fitness_level.lower()

    plan = {
        "summary": "",
        "schedule": [],
        "guidelines": [],
    }

    if "stress" in goal:
        intensities = ["Very Light", "Light", "Moderate"]
        activities_pool = ["Yoga Flow", "Walking", "Breathing Exercises", "Stretching"]
        plan["summary"] = (
            f"To help with stress, this plan focuses on consistent, {intensities[1].lower()} movement to regulate cortisol."
        )
    elif "muscle" in goal or "strength" in goal:
        intensities = ["Moderate", "Hard"]
        activities_pool = ["Bodyweight Strength", "Resistance Training", "Calisthenics"]
        plan["summary"] = "Focus on progressive overload with strength movements."
    else:
        intensities = ["Light", "Moderate"]
        activities_pool = ["Brisk Walking", "Circuit Training", "Cardio"]
        plan["summary"] = "A balanced mix of cardio and light resistance to boost metabolism."

    if fitness_level == "beginner":
        base_duration = min(minutes_per_day, 20)
        activities_pool = [a for a in activities_pool if "Hard" not in a]
    elif fitness_level == "intermediate":
        base_duration = min(minutes_per_day, 40)
    else:
        base_duration = minutes_per_day

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if days_per_week >= 5:
        workout_indices = [0, 1, 2, 3, 4]
    elif days_per_week == 4:
        workout_indices = [0, 2, 4, 6]
    elif days_per_week == 3:
        workout_indices = [0, 2, 4]
    else:
        workout_indices = range(days_per_week)

    for i, day_name in enumerate(week_days):
        day_plan = {"day": day_name}
        if i in workout_indices:
            activity = activities_pool[i % len(activities_pool)]
            day_plan.update(
                {
                    "type": "Workout",
                    "activity": activity,
                    "duration": f"{base_duration} mins",
                    "intensity": intensities[0] if i == 0 else intensities[1 % len(intensities)],
                }
            )
        else:
            day_plan.update(
                {
                    "type": "Rest",
                    "activity": "Light active recovery (optional walk)",
                    "duration": "-",
                }
            )
        plan["schedule"].append(day_plan)

    plan["guidelines"].append("Hydrate before and after sessions.")
    if injuries and injuries.lower() != "none":
        plan["guidelines"].append(f"CAUTION: Modify exercises to accommodate your {injuries}.")
        plan["summary"] += f" Please be careful with your {injuries}."

    if "stress" in goal:
        plan["guidelines"].append("Focus on deep breathing during movement.")

    return plan


def generate_workout_plan(
    goal: str,
    minutes_per_day: int,
    days_per_week: int,
    fitness_level: str,
    injuries: str = "none",
    tool_context: ToolContext | None = None,
) -> Dict:
    """Long-running tool entrypoint – enqueues plan generation job."""

    if tool_context is None:
        # Fallback so the tool can still be invoked synchronously in tests.
        return build_workout_plan(goal, minutes_per_day, days_per_week, fitness_level, injuries)

    ticket_id = str(uuid.uuid4())
    function_call_id = tool_context.function_call_id or ticket_id

    job_store.add(
        PendingJob(
            ticket_id=ticket_id,
            invocation_id=tool_context.invocation_id,
            function_call_id=function_call_id,
            user_id=tool_context.user_id,
            session_id=tool_context.session.id,
            params={
                "goal": goal,
                "minutes_per_day": minutes_per_day,
                "days_per_week": days_per_week,
                "fitness_level": fitness_level,
                "injuries": injuries,
            },
        )
    )

    tool_context.actions.skip_summarization = True

    return {
        "status": "accepted",
        "ticket_id": ticket_id,
        "message": "Great! I'll craft your plan and share it shortly.",
    }


# A2A tool: request mindfulness advice from the Mindfulness Agent via A2A protocol
def get_mindfulness_advice(user_query: str) -> Dict:
    """
    Calls the Mindfulness Agent via A2A protocol to get mindfulness advice.
    This enables the Exercise Agent to incorporate mindfulness suggestions into a holistic plan.
    
    Args:
        user_query: The question or request to send to the mindfulness agent
    
    Returns:
        Dictionary containing the mindfulness advice response
    """
    import requests
    import json
    
    # URL of the mindfulness agent A2A server (running on port 8001)
    MINDFULNESS_AGENT_URL = "http://localhost:8001"
    
    try:
        # First, get the agent card to understand capabilities
        agent_card_response = requests.get(
            f"{MINDFULNESS_AGENT_URL}/.well-known/agent.json",
            timeout=5
        )
        
        if agent_card_response.status_code != 200:
            return {
                "error": "Mindfulness agent not available",
                "advice": "Focus on deep breathing and gentle movement during your workouts."
            }
        
        # Send task to the mindfulness agent
        task_payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tasks/send",
            "params": {
                "task": {
                    "input": {
                        "text": user_query
                    }
                }
            }
        }
        
        task_response = requests.post(
            f"{MINDFULNESS_AGENT_URL}/tasks/send",
            json=task_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if task_response.status_code == 200:
            result = task_response.json()
            # Extract the response text from the A2A response
            if "result" in result and "output" in result["result"]:
                advice = result["result"]["output"].get("text", "")
                return {"advice": advice}
        
        # Fallback if request fails
        return {
            "advice": "Consider incorporating mindfulness practices like deep breathing or meditation into your routine."
        }
        
    except Exception as e:
        # Fallback response if mindfulness agent is unavailable
        return {
            "error": str(e),
            "advice": "Remember to stay present and mindful during your workouts. Focus on your breath and body sensations."
        }
