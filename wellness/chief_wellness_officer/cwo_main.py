"""
Chief Wellness Officer Server - A2A Implementation
Run this to start the CWO as an A2A server on port 8002.
"""

import os
from dotenv import load_dotenv
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from .cwo_agent import chief_wellness_officer

load_dotenv()

APP_NAME = "wellness_orchestrator"

# Configure the ADK app
app_config = App(
    name=APP_NAME,
    root_agent=chief_wellness_officer,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

# Create session service and runner
session_service = InMemorySessionService()
runner = Runner(
    app=app_config,
    session_service=session_service,
)

# Export for A2A
# Run command: adk api_server --a2a --app chief_wellness_officer.main:app_config --port 8002

if __name__ == "__main__":
    print("To run the CWO as an A2A server, use:")
    print("adk api_server --a2a --app chief_wellness_officer.main:app_config --port 8002")
