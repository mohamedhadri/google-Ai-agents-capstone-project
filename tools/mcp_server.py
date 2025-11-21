import json
from fastapi import FastAPI, HTTPException
import uvicorn
import os

app = FastAPI(title="Istanbul Hidden Gems MCP Server")

# Load data
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/hidden_gems.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.get("/gems")
def get_gems(location: str = None):
    data = load_data()
    if location:
        return [item for item in data if item["location"].lower() == location.lower()]
    return data

@app.get("/gems/{name}")
def get_gem_by_name(name: str):
    data = load_data()
    for item in data:
        if item["name"].lower() == name.lower():
            return item
    raise HTTPException(status_code=404, detail="Gem not found")

if __name__ == "__main__":
    # Run on a specific port to act as our "Microservice"
    uvicorn.run(app, host="127.0.0.1", port=8000)
