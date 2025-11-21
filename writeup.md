# Capstone Submission: The Istanbul Insider

## 1. Problem & Solution

**Problem**: Standard travel AI agents often "hallucinate" logistics—suggesting restaurants that are closed, travel times that are impossible, or generic tourist traps. They lack the "local knowledge" and "common sense" of a real concierge.

**Solution**: "The Istanbul Insider" is a multi-agent system that solves this by implementing a **Critic Loop**. A specialized "Critic Agent" reviews every plan for logical errors (time, distance, opening hours) and rejects them if they fail. Additionally, a custom **Model Context Protocol (MCP) Server** injects private, curated "Hidden Gems" into the context, ensuring the itinerary feels unique and premium.

## 2. Key Concepts Applied

### A. Multi-Agent System (Loop & Sequential)

I implemented a sequential chain that turns into a loop upon failure.

- **The Architect** creates the plan.
- **The Critic** evaluates it.
- **The Loop**: If the Critic rejects the plan, the feedback is fed back to the Architect for a retry. This "Self-Correction" pattern significantly reduces hallucinations.

### B. Tools & MCP

I built a **Custom MCP Server** using FastAPI to serve a private database of "Hidden Gems" (e.g., specific non-touristy cafes).

- **Server**: `tools/mcp_server.py` runs a local API.
- **Tool**: `tools/gems_tool.py` allows the Architect Agent to query this private knowledge base, demonstrating how to bridge LLMs with proprietary data.

### C. Agent Evaluation

The **Critic Agent** acts as a real-time evaluator. Instead of evaluating offline, the evaluation happens _during_ the inference process, ensuring the final output is already pre-validated.

## 3. Value Proposition

This agent reduces the time spent fact-checking AI itineraries. By having an automated "Critic," users get a plan that is not just creative, but _logistically viable_, saving hours of frustration when they actually arrive at the destination.
