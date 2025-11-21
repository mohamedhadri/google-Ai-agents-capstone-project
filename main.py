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
    # We use sys.executable to ensure we use the same python interpreter
    server_path = os.path.join(os.path.dirname(__file__), "tools/mcp_server.py")
    process = subprocess.Popen([sys.executable, server_path], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    time.sleep(2) # Give it a moment to start
    return process

def main():
    print("🌍 Welcome to The Istanbul Insider!")
    print("Initializing Agents...")
    
    # Start MCP Server
    mcp_process = start_mcp_server()
    
    try:
        # Initialize Agents
        scout = ScoutAgent()
        architect = ArchitectAgent()
        critic = CriticAgent()
        
        user_request = input("\nWhere do you want to go? (e.g., 'Plan a 1-day trip to Istanbul'): ")
        if not user_request:
            user_request = "Plan a 1-day trip to Istanbul for a history buff."
            
        print(f"\n🎯 Goal: {user_request}\n")
        
        # Step 1: Scout (Optional - just to demonstrate multi-agent)
        # In a real app, Architect might call Scout, but here we'll chain them.
        print("--- Step 1: Scouting ---")
        scout_info = scout.send_message(f"Find key information about: {user_request}")
        print(f"\n📋 Scout Report:\n{scout_info}\n")
        
        # Step 2: Architect & Critic Loop
        max_retries = 3
        current_plan = None
        
        for i in range(max_retries):
            print(f"--- Step 2: Planning (Attempt {i+1}) ---")
            
            if i == 0:
                # First attempt
                prompt = f"Create an itinerary based on this request: '{user_request}'.\nHere is some context from the Scout:\n{scout_info}"
            else:
                # Retry with feedback
                prompt = f"Here is the feedback from the Critic. Please rewrite the plan to fix these issues:\n{critic_feedback}"
            
            current_plan = architect.send_message(prompt)
            print(f"\n📝 Architect's Plan:\n{current_plan}\n")
            
            print("--- Step 3: Critiquing ---")
            critic_feedback = critic.send_message(f"Review this itinerary:\n{current_plan}")
            print(f"\n🧐 Critic's Verdict:\n{critic_feedback}\n")
            
            if "APPROVED" in critic_feedback.upper():
                print("✅ Plan Approved!")
                break
            else:
                print("❌ Plan Rejected. Looping back to Architect...")
        
        if "APPROVED" not in critic_feedback.upper():
            print("⚠️ Could not reach a perfect plan after max retries. Here is the best version:")
            print(current_plan)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\n🛑 Shutting down MCP Server...")
        mcp_process.terminate()

if __name__ == "__main__":
    main()
