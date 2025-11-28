"""Nutrition-specific tool functions used by the Nutrition Agent."""

from __future__ import annotations

from typing import Dict, List, Optional


_ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very active": 1.9,
}


def _mifflin_st_jeor_bmr(age: int, gender: str, weight: float, height: float) -> float:
    """Calculate resting metabolic rate using the Mifflin-St Jeor equation."""
    gender = (gender or "unspecified").lower()
    base = 10 * weight + 6.25 * height - 5 * age
    if gender.startswith("m"):
        return base + 5
    if gender.startswith("f"):
        return base - 161
    return base - 78  # neutral offset for non-binary/unspecified


def _calorie_target(bmr: float, goal: str, activity_level: str) -> int:
    activity = _ACTIVITY_MULTIPLIERS.get(activity_level.lower(), _ACTIVITY_MULTIPLIERS["moderate"])
    maintenance = bmr * activity

    goal = (goal or "wellness").lower()
    if any(keyword in goal for keyword in ("lose", "cut", "deficit", "fat")):
        maintenance -= 400
    elif any(keyword in goal for keyword in ("gain", "muscle", "bulk")):
        maintenance += 250

    return max(int(round(maintenance)), 1200)


def _macro_breakdown(calories: int, weight: float, goal: str) -> Dict[str, Dict[str, int]]:
    goal = goal.lower()
    protein_factor = 1.6
    if any(k in goal for k in ("gain", "muscle", "strength")):
        protein_factor = 1.9
    elif any(k in goal for k in ("lose", "fat", "cut")):
        protein_factor = 1.7

    protein_grams = int(round(protein_factor * weight))
    protein_cal = protein_grams * 4

    fat_ratio = 0.25 if "lose" in goal else 0.3
    fat_cal = calories * fat_ratio
    fat_grams = int(round(fat_cal / 9))

    carb_cal = max(calories - protein_cal - fat_cal, calories * 0.35)
    carb_grams = int(round(carb_cal / 4))

    return {
        "protein": {"grams": protein_grams, "calories": protein_grams * 4},
        "carbs": {"grams": carb_grams, "calories": carb_grams * 4},
        "fat": {"grams": fat_grams, "calories": fat_grams * 9},
    }


def _bmi(height_cm: float, weight: float) -> Dict[str, float | str]:
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "normal"
    elif bmi < 30:
        category = "overweight"
    else:
        category = "obese"
    return {"value": round(bmi, 1), "category": category}


def _meal_suggestions(goal: str, dietary_preference: Optional[str]) -> List[Dict[str, str]]:
    preference = (dietary_preference or "balanced").lower()
    plant_forward = "veg" in preference or "plant" in preference

    meals = [
        {
            "meal": "Breakfast",
            "idea": "Overnight oats with chia, berries, and "+
            ("soy yogurt" if plant_forward else "Greek yogurt"),
            "focus": "Slow-release carbs + protein to stabilize morning energy.",
        },
        {
            "meal": "Lunch",
            "idea": (
                "Quinoa bowl with roasted vegetables, chickpeas, and tahini"
                if plant_forward
                else "Grilled salmon, quinoa, mixed greens, olive oil vinaigrette"
            ),
            "focus": "High protein + colorful vegetables for micronutrients.",
        },
        {
            "meal": "Snack",
            "idea": "Apple slices with almond butter"
            if plant_forward
            else "Greek yogurt parfait with nuts and seeds",
            "focus": "Keeps blood sugar steady between meals.",
        },
        {
            "meal": "Dinner",
            "idea": (
                "Lentil curry with brown rice and steamed greens"
                if plant_forward
                else "Lean turkey stir-fry with brown rice and mixed veggies"
            ),
            "focus": "Fiber-rich carbs for recovery and satiety.",
        },
    ]

    if any(k in goal.lower() for k in ("muscle", "gain")):
        meals.append(
            {
                "meal": "Post-workout",
                "idea": "Protein smoothie with banana, spinach, and flax seeds",
                "focus": "Protein + carbs within 60 minutes of training.",
            }
        )

    return meals


def generate_nutrition_plan(
    age: int,
    gender: str,
    weight: float,
    height: float,
    goal: str,
    dietary_preference: Optional[str] = None,
    allergies: Optional[str] = None,
    activity_level: str = "moderate",
) -> Dict[str, object]:
    """Return a personalized nutrition plan leveraging demographic data."""

    if min(age, weight, height) <= 0:
        raise ValueError("Age, weight, and height must be positive values.")

    bmr = _mifflin_st_jeor_bmr(age=age, gender=gender, weight=weight, height=height)
    calories = _calorie_target(bmr=bmr, goal=goal, activity_level=activity_level)
    macros = _macro_breakdown(calories=calories, weight=weight, goal=goal)
    bmi = _bmi(height_cm=height, weight=weight)

    plan = {
        "profile_summary": {
            "age": age,
            "gender": gender,
            "weight_kg": weight,
            "height_cm": height,
            "bmi": bmi,
        },
        "goal": goal,
        "calorie_target": calories,
        "macros": macros,
        "meal_suggestions": _meal_suggestions(goal=goal, dietary_preference=dietary_preference),
        "hydration": "Aim for {:.1f} L/day".format(max(round(weight * 0.035, 1), 2.0)),
        "allergy_notes": allergies or "None reported",
        "tips": [
            "Distribute protein evenly across meals to maximize muscle protein synthesis.",
            "Prioritize whole foods and high-fiber carbs to keep you fuller longer.",
            "Pair hydration reminders with meals to build consistency.",
        ],
    }

    if bmi["category"] in {"underweight", "obese"}:
        plan["tips"].append(
            "Work with a registered dietitian if your BMI is outside the moderate range for extended periods."
        )

    if dietary_preference:
        plan["notes"] = f"Plan biased toward {dietary_preference} choices."

    return plan
