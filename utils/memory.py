import json
import os
from typing import List, Dict, Any
from datetime import datetime

class MemoryManager:
    def __init__(self, history_file: str = "data/history.json", max_sessions: int = 3):
        self.history_file = history_file
        self.max_sessions = max_sessions
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensures the data directory and history file exist."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                json.dump([], f)

    def load_memory(self) -> List[Dict[str, Any]]:
        """Loads the session history from the JSON file."""
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_session(self, session_id: str, messages: List[Dict[str, str]], title: str = None):
        """Saves the current session to history, enforcing the limit."""
        if not messages:
            return

        history = self.load_memory()
        
        # Check if session exists
        session_index = -1
        existing_title = None
        for i, session in enumerate(history):
            if session.get("session_id") == session_id:
                session_index = i
                existing_title = session.get("title")
                break
        
        # Use new title if provided, otherwise keep existing, otherwise None
        final_title = title if title else existing_title

        session_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "title": final_title,
            "messages": messages
        }
        
        if session_index >= 0:
            # Update existing session
            history[session_index] = session_data
        else:
            # Add new session
            history.append(session_data)
        
        # Enforce limit (keep last N sessions)
        if len(history) > self.max_sessions:
            history = history[-self.max_sessions:]
            
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)

    def get_memory_context(self) -> str:
        """Returns a summarized string of past sessions for the LLM."""
        history = self.load_memory()
        if not history:
            return ""
            
        context = "PREVIOUS CONVERSATION HISTORY (for context only):\n"
        for i, session in enumerate(history):
            context += f"--- Session {i+1} ({session['timestamp']}) ---\n"
            # Limit to last 5 messages per session to save tokens, or summarize
            # For now, we'll just take the user messages and assistant responses
            for msg in session['messages']:
                role = msg['role'].upper()
                content = msg['content']
                # Skip system messages or internal tool outputs if any
                if role in ["USER", "ASSISTANT"]:
                    context += f"{role}: {content}\n"
            context += "\n"
            
        return context
