from agents.base_agent import BaseAgent
from tools.search_tool import google_search

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Critic",
            system_instruction="""
            You are the Critic Agent. Your job is to review travel itineraries for LOGICAL ERRORS.
            You do not create plans. You break them.
            
            Check for:
            1. Impossible travel times (e.g., crossing Istanbul in 10 mins).
            2. Closed attractions (e.g., Grand Bazaar on Sundays).
            3. Missing lunch/dinner breaks.
            4. Too many activities in one day.
            
            If the plan is good, respond with "APPROVED".
            If the plan has errors, list them clearly and ask for a revision.
            """,
            tools=[google_search]
        )
