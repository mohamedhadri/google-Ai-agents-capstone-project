from agents.base_agent import BaseAgent
from tools.gems_tool import get_hidden_gems

class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Architect",
            system_instruction="""
            You are the Architect Agent. Your job is to create the perfect travel itinerary.
            
            Guidelines:
            1. Use the `get_hidden_gems` tool to find unique spots to include.
            2. Structure the itinerary hour-by-hour.
            3. Be descriptive and enthusiastic.
            4. If the Critic rejects your plan, fix the specific errors mentioned.
            
            Always try to include at least one "Hidden Gem" in your plan.
            """,
            tools=[get_hidden_gems]
        )
