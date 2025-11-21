import requests

def get_hidden_gems(location: str):
    """
    Queries the local 'Hidden Gems' server to find unique, non-touristy spots.
    Use this to add special flair to the itinerary.
    """
    try:
        # Connect to our local MCP server
        response = requests.get(f"http://127.0.0.1:8000/gems?location={location}")
        if response.status_code == 200:
            gems = response.json()
            if not gems:
                return f"No hidden gems found for {location}."
            
            # Format the output nicely
            result = f"💎 Hidden Gems in {location}:\n"
            for gem in gems:
                result += f"- {gem['name']} ({gem['type']}): {gem['description']} [Price: {gem['price']}]\n"
            return result
        else:
            return f"Error querying MCP server: {response.status_code}"
    except Exception as e:
        return f"Could not connect to Hidden Gems server. Is it running? Error: {str(e)}"
