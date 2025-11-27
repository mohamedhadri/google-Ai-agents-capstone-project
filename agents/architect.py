from agents.base_agent import BaseAgent
from tools.gems_tool import get_hidden_gems

class ArchitectAgent(BaseAgent):
    def __init__(self, memory_context: str = ""):
        instruction = """
            You are the Architect Agent. Your job is to create the perfect travel itinerary.
            
            Guidelines:
            1. Use the `get_hidden_gems` tool to find unique spots to include.
            2. Structure the itinerary hour-by-hour.
            3. Be descriptive and enthusiastic.
            4. If the Critic rejects your plan, fix the specific errors mentioned.
            5. **Defaults**:
                - If the user does not specify the duration, assume a **1-day trip**.
                - If the user does not specify a budget, assume a **moderate budget** but suggest they provide one for better accuracy.
            
            Always try to include at least one "Hidden Gem" in your plan.
            """
        
        if memory_context:
            instruction += f"\n\n{memory_context}"

        super().__init__(
            name="Architect",
            model_name="gemini-1.5-pro",
            system_instruction=instruction,
            tools=[get_hidden_gems]
        )
