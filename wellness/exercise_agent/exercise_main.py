"""
Exercise Agent Server - A2A Implementation
This file exposes the exercise agent via the A2A protocol.
Run this to start the exercise agent as an A2A server on port 8000.
"""

import os
import uvicorn
from dotenv import load_dotenv
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from .exercise_agent import exercise_agent

load_dotenv()

APP_NAME = "exercise_app"

# Configure the ADK app
app_config = App(
    name=APP_NAME,
    root_agent=exercise_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

# Create session service and runner
session_service = InMemorySessionService()
runner = Runner(
    app=app_config,
    session_service=session_service,
)

# Export the configured app to be used with A2A
# To run this agent as an A2A server:
# Run the command: adk api_server --a2a --app exercise_agent.main:app_config --port 8000

if __name__ == "__main__":
    # For non-A2A testing, you can run a simple FastAPI server here
    # But for A2A, use the adk api_server command
    print("To run this agent as an A2A server, use:")
    print("adk api_server --a2a --app exercise_agent.main:app_config --port 8000")
