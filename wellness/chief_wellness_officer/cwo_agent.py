"""
Chief Wellness Officer Agent
The orchestrator agent that routes user requests to the appropriate specialist.
"""

import textwrap
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .cwo_tools import consult_exercise_specialist, consult_mindfulness_specialist

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

chief_wellness_officer = Agent(
    name="chief_wellness_officer",
    model=Gemini(model="gemini-2.5-pro", retry_options=retry_config), # Stronger model for reasoning/routing
    tools=[consult_exercise_specialist, consult_mindfulness_specialist],
    description="The Chief Wellness Officer that orchestrates the user's wellness journey.",
    instruction=textwrap.dedent(
        """
        You are the Chief Wellness Officer (CWO) for a holistic wellness application.
        
        Your Goal:
        1. Understand the user's overall wellness needs.
        2. Route specific requests to your specialist agents:
           - Use `consult_exercise_specialist` for physical activity, workouts, and fitness goals.
           - Use `consult_mindfulness_specialist` for stress, anxiety, meditation, and mental well-being.
        3. Synthesize the responses from your specialists into a cohesive, helpful answer for the user.
        
        Process:
        - If the user has a complex goal (e.g., "I want to lose weight and reduce stress"), you should call BOTH specialists and combine their advice.
        - If the user greets you, welcome them warmly as the Chief Wellness Officer and ask how you can support their wellness journey today.
        - Always maintain a supportive, professional, and holistic tone.
        """
    ),
)
