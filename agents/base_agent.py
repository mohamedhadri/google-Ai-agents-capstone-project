import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, model_name: str = "gemini-2.0-flash-exp", system_instruction: str = "", tools: list = None):
        self.name = name
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.tools = tools or []
        self.history = []
        
        # Configure API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
        genai.configure(api_key=api_key)
        
        # Initialize Model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction,
            tools=self.tools
        )
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message: str):
        """Sends a message to the agent and returns the response."""
        print(f"🤖 [{self.name}] Thinking...")
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        return self.chat.history
