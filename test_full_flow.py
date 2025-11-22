import time
import subprocess
import sys
import os
from agents.scout import ScoutAgent
from agents.architect import ArchitectAgent
from agents.critic import CriticAgent
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def start_mcp_server():
    """Starts the MCP server in a background process."""
    print("🚀 Starting Local MCP Server...")
    server_path = os.path.join(os.path.dirname(__file__), "tools/mcp_server.py")
    process = subprocess.Popen([sys.executable, server_path], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    time.sleep(2) # Give it a moment to start
    return process

def test_run():
    print("🧪 Starting Automated Test Run...")
    
    # Start MCP Server
    mcp_process = start_mcp_server()
    
    try:
        # Initialize Agents
        print("🔹 Initializing Agents...")
        scout = ScoutAgent()
        architect = ArchitectAgent()
        critic = CriticAgent()
        
        test_request = "Plan a 1-day trip to Istanbul for a history buff."
        print(f"🎯 Test Goal: {test_request}\n")
        
        # Step 1: Scout
        print("--- Step 1: Scouting ---")
        scout_info = scout.send_message(f"Find key information about: {test_request}")
        print(f"📋 Scout Report (First 200 chars): {scout_info[:200]}...\n")
        
        # Step 2: Architect
        print("--- Step 2: Planning ---")
        prompt = f"Create an itinerary based on this request: '{test_request}'.\nHere is some context from the Scout:\n{scout_info}"
        plan = architect.send_message(prompt)
        print(f"📝 Architect's Plan (First 200 chars): {plan[:200]}...\n")
        
        # Step 3: Critic
        print("--- Step 3: Critiquing ---")
        critique = critic.send_message(f"Review this itinerary:\n{plan}")
        print(f"🧐 Critic's Verdict: {critique}\n")
        
        print("✅ Test Completed Successfully!")
            
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🛑 Shutting down MCP Server...")
        mcp_process.terminate()

if __name__ == "__main__":
    test_run()
