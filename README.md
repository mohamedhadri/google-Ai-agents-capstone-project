# The Istanbul Insider 🇹🇷

### Google AI Agents Capstone Project

**Track:** Concierge Agents
**Author:** Mohamed Hadri

![App Screenshot](assets/app_screenshot.png)

## Overview

"The Istanbul Insider" is a multi-agent travel orchestrator that goes beyond simple itinerary generation. It features a **Self-Correcting Loop** where a "Critic Agent" validates plans against real-world logic, and a **Local MCP Server** that injects private "Hidden Gem" knowledge that standard LLMs might miss.

## Key Features (Course Concepts Applied)

1.  **Multi-Agent System**:
    - **Scout**: Gathers raw information.
    - **Architect**: Plans the itinerary.
    - **Critic**: Validates the plan (Loop Agent).
    - **Guard**: Filters off-topic requests and handles greetings.
2.  **Tools & MCP**:
    - **Custom MCP Server**: A local FastAPI server providing "Hidden Gems" data.
    - **Search Tool**: For real-time info.
3.  **Sessions & Memory**:
    - Agents maintain history context throughout the planning loop.
    - The system remembers the current plan for iterative improvements.

## Setup & Run

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    - Create a `.env` file in the root directory.
    - Add your Gemini API key:
      ```
      GOOGLE_API_KEY=your_api_key_here
      ```

3.  **Run the Agent**:
    ```bash
    streamlit run app.py
    ```

## Architecture

- `app.py`: The main Streamlit web application (UI) and agent orchestrator.
- `agents/`: Contains the `BaseAgent` (ADK-style wrapper) and specialized agents (`Scout`, `Architect`, `Critic`, `Guard`).
- `tools/`: Contains the MCP server (`mcp_server.py`) and client tools.
- `data/`: Contains the JSON database for the MCP server.
