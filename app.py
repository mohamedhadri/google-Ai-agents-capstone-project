import streamlit as st
import subprocess
import sys
import os
import time
import atexit
from agents.scout import ScoutAgent
from agents.architect import ArchitectAgent
from agents.critic import CriticAgent
from agents.guard import GuardAgent
from agents.summary import SummaryAgent
from utils.memory import MemoryManager
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

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Session State for Rate Limiting
if "rate_limit" not in st.session_state:
    st.session_state.rate_limit = {
        "count": 0,
        "start_time": time.time()
    }

import uuid

# Session State for Current Plan (Memory)
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None

# Session State for Session Title
if "session_title" not in st.session_state:
    st.session_state.session_title = None

# Initialize Memory Manager
if "memory_manager" not in st.session_state:
    st.session_state.memory_manager = MemoryManager()
    st.session_state.memory_context = st.session_state.memory_manager.get_memory_context()
    st.session_state.session_id = str(uuid.uuid4())

def check_rate_limit():
    """Checks if the user has exceeded the rate limit (3 requests per hour)."""
    limit = 3
    duration = 3600 # 1 hour
    
    current_time = time.time()
    elapsed = current_time - st.session_state.rate_limit["start_time"]
    
    if elapsed > duration:
        # Reset if hour has passed
        st.session_state.rate_limit["count"] = 0
        st.session_state.rate_limit["start_time"] = current_time
    
    if st.session_state.rate_limit["count"] >= limit:
        remaining = int((duration - elapsed) / 60)
        return False, f"Rate limit exceeded. You have used {limit} requests. Please wait {remaining} minutes."
    
    return True, None

def increment_rate_limit():
    """Increments the request count."""
    st.session_state.rate_limit["count"] += 1

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
    
    # Display Rate Limit Status
    count = st.session_state.rate_limit["count"]
    st.metric("Requests Used (1h)", f"{count}/3")

    st.divider()
    st.header("History")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.current_plan = None
        st.session_state.session_title = None
        st.rerun()
    
    # List Previous Sessions
    sessions = st.session_state.memory_manager.load_memory()
    # Show most recent first
    for s in reversed(sessions):
        # Get Session ID safely
        session_id = s.get("session_id")
        if not session_id:
            continue

        # Determine title
        title = s.get("title")
        if not title:
            # Fallback to timestamp or first message
            title = s["timestamp"]
            if s["messages"]:
                for m in s["messages"]:
                    if m["role"] == "user":
                        # Truncate to 30 chars
                        content = m["content"]
                        title = (content[:27] + '...') if len(content) > 27 else content
                        break
        
        # Highlight current session
        type_ = "primary" if session_id == st.session_state.session_id else "secondary"
        
        if st.button(title, key=session_id, use_container_width=True, type=type_):
            st.session_state.session_id = session_id
            st.session_state.messages = s["messages"]
            st.session_state.current_plan = None # Reset plan state
            st.session_state.session_title = s.get("title")
            st.rerun()

# Start Server
with st.spinner("Starting Local MCP Server..."):
    start_mcp_server()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Where do you want to go? (e.g., Plan a 2-day trip to Istanbul)"):
    # Check Rate Limit
    allowed, error_msg = check_rate_limit()
    
    if not allowed:
        st.error(error_msg)
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            try:
                increment_rate_limit()
                
                # Initialize Guard
                guard = GuardAgent(memory_context=st.session_state.memory_context)
                with st.spinner("Thinking..."):
                    # Pass current plan context to Guard if available
                    guard_prompt = prompt
                    if st.session_state.current_plan:
                        guard_prompt = f"Current Plan: {st.session_state.current_plan}\nUser Request: {prompt}"
                    
                    guard_response = guard.send_message(guard_prompt)
                
                # Determine Action
                action = "CHAT"
                if "NEW_PLAN" in guard_response:
                    action = "NEW_PLAN"
                elif "MODIFY" in guard_response:
                    action = "MODIFY"
                
                if action == "CHAT":
                    st.markdown(guard_response)
                    st.session_state.messages.append({"role": "assistant", "content": guard_response})
                    
                    # Generate Title if needed
                    if not st.session_state.session_title and len(st.session_state.messages) >= 2:
                        summary_agent = SummaryAgent()
                        st.session_state.session_title = summary_agent.generate_title(st.session_state.messages)
                    
                    st.session_state.memory_manager.save_session(st.session_state.session_id, st.session_state.messages, st.session_state.session_title)
                
                else:
                    # Initialize Agents
                    scout = ScoutAgent()
                    architect = ArchitectAgent(memory_context=st.session_state.memory_context)
                    critic = CriticAgent()

                    # Container for the "Thinking" process
                    with st.status("🤖 Agent is working...", expanded=False) as status:
                        
                        scout_info = ""
                        
                        # Handle NEW_PLAN vs MODIFY
                        if action == "NEW_PLAN":
                            st.session_state.current_plan = None # Reset
                            st.write("🔍 **Scout** is gathering information...")
                            scout_info = scout.send_message(f"Find key information about: {prompt}")
                            with st.expander("See Scout Report"):
                                st.markdown(scout_info)
                            
                            initial_prompt = f"Create an itinerary based on this request: '{prompt}'.\nHere is some context from the Scout:\n{scout_info}"
                        
                        elif action == "MODIFY":
                            st.write("🔄 **Architect** is updating the plan...")
                            initial_prompt = f"Update this plan:\n{st.session_state.current_plan}\n\nBased on this request:\n{prompt}"

                        # Architect & Critic Loop
                        max_retries = 3
                        current_plan = None
                        final_plan = None
                        
                        for i in range(max_retries):
                            st.write(f"🏗️ **Architect** is planning (Attempt {i+1})...")
                            
                            if i == 0:
                                plan_prompt = initial_prompt
                            else:
                                plan_prompt = f"Here is the feedback from the Critic. Please rewrite the plan to fix these issues:\n{critic_feedback}"
                            
                            current_plan = architect.send_message(plan_prompt)
                            
                            st.write(f"🧐 **Critic** is reviewing...")
                            critic_feedback = critic.send_message(f"Review this itinerary:\n{current_plan}")
                            
                            with st.expander(f"Attempt {i+1} Details"):
                                st.markdown("**Plan:**")
                                st.markdown(current_plan)
                                st.markdown("**Critic's Verdict:**")
                                st.markdown(critic_feedback)
                            
                            if "APPROVED" in critic_feedback.upper():
                                final_plan = current_plan
                                status.update(label="✅ Plan Approved!", state="complete", expanded=False)
                                break
                            else:
                                st.write("❌ Plan rejected, retrying...")
                        
                        if not final_plan:
                            final_plan = current_plan
                            status.update(label="⚠️ Plan finalized with warnings", state="complete", expanded=False)

                    # Update Memory
                    st.session_state.current_plan = final_plan

                    # Display Final Result
                    st.markdown(final_plan)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": final_plan})
                    
                    # Generate Title if needed
                    if not st.session_state.session_title:
                        summary_agent = SummaryAgent()
                        st.session_state.session_title = summary_agent.generate_title(st.session_state.messages)
                        
                    st.session_state.memory_manager.save_session(st.session_state.session_id, st.session_state.messages, st.session_state.session_title)

            except Exception as e:
                st.error(f"An error occurred: {e}")
