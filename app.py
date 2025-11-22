import streamlit as st
import subprocess
import sys
import os
import time
import atexit
from agents.scout import ScoutAgent
from agents.architect import ArchitectAgent
from agents.critic import CriticAgent
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Page Config
st.set_page_config(
    page_title="The Istanbul Insider",
    page_icon="🌍",
    layout="centered"
)

# Session State for MCP Server
if 'mcp_server_process' not in st.session_state:
    st.session_state.mcp_server_process = None

def start_mcp_server():
    """Starts the MCP server in a background process."""
    if st.session_state.mcp_server_process is None:
        server_path = os.path.join(os.path.dirname(__file__), "tools/mcp_server.py")
        # Use sys.executable to ensure same python environment
        process = subprocess.Popen([sys.executable, server_path], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        st.session_state.mcp_server_process = process
        time.sleep(2) # Warmup
        return True
    return False

def stop_mcp_server():
    """Stops the MCP server."""
    if st.session_state.mcp_server_process:
        st.session_state.mcp_server_process.terminate()
        st.session_state.mcp_server_process = None

# Register cleanup
atexit.register(stop_mcp_server)

# UI Header
st.title("🌍 The Istanbul Insider")
st.markdown("### Your AI Travel Concierge for Turkey")

# Sidebar for API Key (Optional for deployment)
with st.sidebar:
    st.header("Configuration")
    if not os.getenv("GOOGLE_API_KEY"):
        api_key = st.text_input("Enter Google API Key", type="password")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
    
    st.info("This agent uses a multi-agent system with a custom MCP server to find hidden gems.")

# Start Server
with st.spinner("Starting Local MCP Server..."):
    start_mcp_server()

# Main Input
user_request = st.text_input("Where do you want to go?", placeholder="e.g., Plan a 2-day trip to Istanbul for a foodie")

if st.button("Plan My Trip"):
    if not user_request:
        st.warning("Please enter a request first.")
    else:
        try:
            # Initialize Agents
            with st.spinner("Initializing Agents..."):
                scout = ScoutAgent()
                architect = ArchitectAgent()
                critic = CriticAgent()

            # Step 1: Scout
            st.subheader("Step 1: Scouting")
            with st.status("Scout Agent is gathering info...", expanded=True) as status:
                scout_info = scout.send_message(f"Find key information about: {user_request}")
                st.markdown(scout_info)
                status.update(label="Scouting Complete", state="complete", expanded=False)

            # Step 2: Architect & Critic Loop
            st.subheader("Step 2: Planning & Critiquing")
            
            max_retries = 3
            current_plan = None
            final_plan = None
            
            progress_bar = st.progress(0)
            
            for i in range(max_retries):
                with st.expander(f"Planning Attempt {i+1}", expanded=True):
                    # Architect
                    st.markdown(f"**🤖 Architect is thinking...**")
                    if i == 0:
                        prompt = f"Create an itinerary based on this request: '{user_request}'.\nHere is some context from the Scout:\n{scout_info}"
                    else:
                        prompt = f"Here is the feedback from the Critic. Please rewrite the plan to fix these issues:\n{critic_feedback}"
                    
                    current_plan = architect.send_message(prompt)
                    st.markdown(current_plan)
                    
                    # Critic
                    st.markdown(f"**🧐 Critic is reviewing...**")
                    critic_feedback = critic.send_message(f"Review this itinerary:\n{current_plan}")
                    st.info(f"Critic's Verdict:\n{critic_feedback}")
                    
                    if "APPROVED" in critic_feedback.upper():
                        st.success("✅ Plan Approved!")
                        final_plan = current_plan
                        progress_bar.progress(100)
                        break
                    else:
                        st.error("❌ Plan Rejected. Retrying...")
                        progress_bar.progress(int((i + 1) / max_retries * 100))
            
            if final_plan:
                st.divider()
                st.header("🎉 Your Final Itinerary")
                st.markdown(final_plan)
                st.balloons()
            else:
                st.warning("Could not reach a perfect plan, but here is the best version:")
                st.markdown(current_plan)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini & Streamlit")
