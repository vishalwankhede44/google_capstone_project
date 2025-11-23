"""
Mindfulness Agent Tools
These are the tools available to the mindfulness agents.
"""

import requests

def get_public_ip() -> str:
    """Return the public IP address of the current machine."""
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return "8.8.8.8"

def get_current_locality() -> str:
    """Return a human-readable location (city, country) for the public IP.
    Falls back to "Unknown Location" on any error.
    """
    ip = get_public_ip()
    if ip == "8.8.8.8":
        return "Unknown Location"
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = resp.json()
        if data.get("status") == "success":
            return f"{data.get('city', 'Unknown City')}, {data.get('country', 'Unknown Country')}"
    except Exception:
        pass
    return "Unknown Location"
