"""
Chief Wellness Officer Tools
These tools allow the CWO to consult specialist agents via A2A protocol.
"""

import requests
import uuid
from typing import Dict

# Configuration for Specialist Agents
EXERCISE_AGENT_URL = "http://localhost:8000"
MINDFULNESS_AGENT_URL = "http://localhost:8001"

def _call_agent(agent_url: str, user_query: str) -> Dict:
    """Helper to call an A2A agent."""
    try:
        # Check agent availability via Agent Card
        card_resp = requests.get(f"{agent_url}/.well-known/agent.json", timeout=2)
        if card_resp.status_code != 200:
             return {"error": f"Agent at {agent_url} is not available."}

        # Send Task
        payload = {
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
        
        resp = requests.post(
            f"{agent_url}/tasks/send",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if resp.status_code == 200:
            data = resp.json()
            if "result" in data and "output" in data["result"]:
                return {"response": data["result"]["output"].get("text", "")}
            if "error" in data:
                return {"error": f"Agent Error: {data['error']}"}
        
        return {"error": f"Request failed with status {resp.status_code}"}

    except Exception as e:
        return {"error": f"Connection failed: {str(e)}"}


def consult_exercise_specialist(user_request: str) -> Dict:
    """
    Consults the Exercise Agent for workout plans and physical activity advice.
    Use this when the user asks about workouts, fitness, strength, or physical health.
    """
    return _call_agent(EXERCISE_AGENT_URL, user_request)


def consult_mindfulness_specialist(user_request: str) -> Dict:
    """
    Consults the Mindfulness Agent for meditation, stress reduction, and mental wellness.
    Use this when the user asks about stress, anxiety, meditation, or mental health.
    """
    return _call_agent(MINDFULNESS_AGENT_URL, user_request)
