from typing import Dict


def build_workout_plan(
    goal: str,
    minutes_per_day: int,
    days_per_week: int,
    fitness_level: str,
    age: int,
    weight: float,
    gender: str,
    injuries: str = "none",
) -> Dict:
    """Deterministically builds the workout plan payload.

    This version uses explicit primitive parameters instead of a Dict so that the
    ADK tool schema remains compatible with the Google GenAI function-calling API.
    """

    goal = goal.lower()
    fitness_level = fitness_level.lower()

    plan = {
        "summary": "",
        "schedule": [],
        "guidelines": [],
        "personalization": f"Plan customized for {gender}, age {age}, weight {weight}kg",
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

    # Age-based adjustments
    if age > 50:
        plan["guidelines"].append("Focus on joint-friendly movements and proper warm-up.")
        plan["summary"] += " Age-appropriate modifications included."
    
    # Weight-based guidance
    if weight > 90:
        plan["guidelines"].append("Consider low-impact exercises to protect joints.")
    
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
    age: int,
    weight: float,
    gender: str,
    injuries: str = "none",
) -> Dict:
    """Generate a personalized workout plan.

    Called by the Exercise Agent. The CWO provides the user's profile information
    (age, weight, gender, fitness_level, injuries) via context so the agent can
    fill these parameters when invoking the tool.
    """

    plan = build_workout_plan(
        goal=goal,
        minutes_per_day=minutes_per_day,
        days_per_week=days_per_week,
        fitness_level=fitness_level,
        age=age,
        weight=weight,
        gender=gender,
        injuries=injuries,
    )

    return plan
