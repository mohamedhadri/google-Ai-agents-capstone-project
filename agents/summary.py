from agents.base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Summary",
            model_name="gemini-2.0-flash",
            system_instruction="""
            You are a Summarizer Agent.
            Your task is to generate a SHORT, concise title (maximum 5 words) for a travel planning conversation.
            Analyze the user's request and the agent's response to understand the topic.
            
            Examples:
            - "Plan a 2-day trip to Istanbul" -> "2-Day Istanbul Itinerary"
            - "Where can I eat vegan food in Ankara?" -> "Vegan Food in Ankara"
            - "Hidden gems in Cappadocia" -> "Cappadocia Hidden Gems"
            
            Output ONLY the title. Do not use quotes.
            """
        )

    def generate_title(self, messages):
        """Generates a title based on the conversation history."""
        # Convert messages to a string format for the LLM
        conversation_text = ""
        for msg in messages[:4]: # Only look at the first few messages
            conversation_text += f"{msg['role']}: {msg['content']}\n"
            
        return self.send_message(f"Generate a title for this conversation:\n{conversation_text}")
