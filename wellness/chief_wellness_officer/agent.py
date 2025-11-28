"""
chief_wellness_officer.agent
ADK expects this file to expose a `root_agent` variable for agent discovery.
"""

from .cwo_agent import chief_wellness_officer

root_agent = chief_wellness_officer

__all__ = ["root_agent"]
