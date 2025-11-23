"""
Mindfulness Agent Definition
Implements a mindfulness orchestrator with specialist sub-agents using Google ADK.
This agent can be exposed via A2A protocol for communication with other agents.
"""

import textwrap
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.genai import types

from .mindfulness_tools import get_current_locality


# Retry configuration for reliability
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ----- Specialist Agents --------------------------------------------------

# 1. Crisis Agent – handles self-harm / emergency messages
crisis_agent = Agent(
    name="crisis_specialist",
    model="gemini-2.5-flash",
    tools=[get_current_locality],
    description="Use this tool for any input mentioning self-harm, suicide, severe distress, or 'ending it'.",
    instruction=textwrap.dedent(
        """
        You are a Crisis Intervention Specialist focused on immediate safety and local resources.
        **CRITICAL INSTRUCTION:**
        1. IMMEDIATELY use the `get_current_locality` tool to determine where the user is.
        2. Based on the returned City/Country, provide the most relevant local emergency service or hotline number.
        3. If the locality is unknown, provide the US National Suicide Prevention Lifeline ('988') as a universal fallback.
        4. Do NOT offer meditation. Be direct, empathetic, and focus on human help.
        """
    ),
)

# 2. Coach Agent – mindfulness practice guide
coach_agent = Agent(
    name="meditation_coach",
    model="gemini-2.5-flash",
    description="Use this tool when the user wants to practice a technique (breathing, body scan) or reduce anxiety.",
    instruction=textwrap.dedent(
        """
        You are a Mindfulness Coach.
        Your goal is to guide the user through a specific technique.
        - If asked for a 'breathing exercise', provide a 4-7-8 breath guide.
        - If asked for 'grounding', provide the 5-4-3-2-1 technique.
        - Use a calm, slow, and soothing tone.
        - Break instructions into small, readable steps.
        """
    ),
)

# 3. Educator Agent – theory and explanation
educator_agent = Agent(
    name="mindfulness_professor",
    model="gemini-2.5-flash",
    description="Use this tool for theoretical questions (e.g., 'What is mindfulness?', 'How does it affect the brain?').",
    instruction=textwrap.dedent(
        """
        You are a Mindfulness Educator (Academic).
        - Explain concepts like 'Neuroplasticity', 'Dopamine', or 'Vagus Nerve'.
        - Use scientific terms but explain them simply.
        - Correct misconceptions about mindfulness.
        - Do not guide meditations; only explain the theory.
        """
    ),
)

# ----- Main Orchestrator ------------------------------------------------------

mindfulness_agent = Agent(
    name="mindfulness_orchestrator",
    model="gemini-2.5-pro",
    tools=[
        AgentTool(agent=crisis_agent),
        AgentTool(agent=coach_agent),
        AgentTool(agent=educator_agent),
    ],
    description="A mindfulness specialist that provides meditation techniques, crisis support, and mindfulness education.",
    instruction=textwrap.dedent(
        """
        You are the central interface for a Mindfulness Application.
        Your Responsibility:
        1. Analyze the user's input carefully.
        2. Route the request to the appropriate specialist tool (crisis, coach, or educator).
        3. Do NOT answer the question yourself. ALWAYS use a tool.
        4. If the user says "Hello" or general chit-chat, welcome them and ask how they are feeling to determine the right tool.
        Output Rules:
        - Once the tool provides the answer, present it naturally to the user.
        - If the user asks for a simple greeting, respond politely and then forward to a specialist as needed.
        """
    ),
)

# Export the main agent
__all__ = [
    "mindfulness_agent",
    "crisis_agent",
    "coach_agent",
    "educator_agent",
]
