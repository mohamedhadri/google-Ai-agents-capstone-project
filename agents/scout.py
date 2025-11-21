from agents.base_agent import BaseAgent
from tools.search_tool import google_search

class ScoutAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Scout",
            system_instruction="""
            You are the Scout Agent. Your job is to find raw information using the Google Search tool.
            You do NOT plan the trip. You only gather facts.
            When asked to find something, use the `google_search` tool.
            Summarize the search results clearly.
            """,
            tools=[google_search]
        )
