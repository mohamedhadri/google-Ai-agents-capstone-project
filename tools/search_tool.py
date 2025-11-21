class SearchTool:
    def search(self, query: str):
        """
        Performs a web search for the given query.
        """
        print(f"🔎 Searching web for: {query}")
        # Mock results for Istanbul to ensure reliability without external API keys
        if "istanbul" in query.lower():
            return """
            Search Results for Istanbul:
            1. Top Attractions: Hagia Sophia, Blue Mosque, Topkapi Palace, Grand Bazaar.
            2. Weather: Mild in spring/autumn, hot summers.
            3. Transport: Trams and ferries are popular.
            4. Food: Kebabs, Baklava, Turkish Delight.
            """
        return "No specific results found for this mock search. Try 'Istanbul'."

# Expose as a function for Gemini
def google_search(query: str):
    """Performs a Google search to find information about places, events, or facts."""
    tool = SearchTool()
    return tool.search(query)
