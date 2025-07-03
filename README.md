# LangGraph Agent Implementations

This repository contains Jupyter notebooks and Python scripts demonstrating various LangGraph agent implementations, focusing on building conversational AI with integrated tools and advanced graph structures.

## Table of Contents

* [openai\_agent.py: OpenAI-Powered Tool-Calling Agent](#openai_agentpy-openai-powered-tool-calling-agent)
* [Setup and Prerequisites](#setup-and-prerequisites)
* [Usage](#usage)

---

## openai\_agent.py: OpenAI-Powered Tool-Calling Agent

This Python script showcases how to build and configure LangGraph agents, including a simple LLM agent and a more advanced tool-calling agent, leveraging OpenAI models.

### Key Concepts Demonstrated:

* **State Definition:** Defining the graph's shared state using `TypedDict`, specifically `messages: Annotated[list[BaseMessage], add_messages]` for robust conversation history management.
* **Default LLM Agent (`make_default_graph`):** Implementation of a basic LangGraph agent where the LLM directly processes messages and returns a response.
* **Tool-Calling Agent (`make_alternative_graph`):** A more advanced agent that demonstrates:
    * **Custom Tools:** Defining Python functions (e.g., `add`) as tools using `@tool` decorator.
    * **`ToolNode`:** Integrating tools into the graph workflow using `ToolNode`.
    * **Model Binding:** Binding tools to the `ChatOpenAI` model (`model.bind_tools()`) so it can generate tool calls.
    * **Conditional Edges:** Implementing dynamic routing based on the LLM's output (`should_continue` function checks for `tool_calls` to decide if more tool execution is needed or if the conversation should end).
* **Environment Variable Loading:** Securely loading API keys using `python-dotenv`.

### Workflow Flow:

* **Default Graph:** `START` -> `agent` (LLM call) -> `END`.
* **Tool-Calling Graph:** `START` -> `agent` (LLM invokes with tools).
    * **Conditional Decision:** If the LLM generates `tool_calls`, the flow goes to `tools` node.
    * **Tool Execution:** The `tools` node executes the specified tools.
    * **Loop Back:** After tool execution, the flow returns to the `agent` node for the LLM to process tool outputs and generate a final response.
    * **End:** If the LLM does not generate `tool_calls` (or after processing tool outputs), the flow ends.

---

## Setup and Prerequisites

To run these files, you will need:

* Python 3.9+
* Jupyter Notebook or JupyterLab (if you convert the `.py` to a notebook, or for general development)
* **OpenAI API Key** (for the `ChatOpenAI` model).
* **Langsmith API Key** (optional, for tracing).

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Abubakar0011/Agent_using_OpenAI.git](https://github.com/Abubakar0011/Agent_using_OpenAI.git) 
    cd LangGraph_Practice
    ```

2.  **Set up Virtual Environment & Install Dependencies:**
    It's highly recommended to use a Python virtual environment. You can use `uv` for faster installation:

    ```bash
    # Install uv if you don't have it
    # pip install uv

    python -m venv .venv
    source .venv/bin/activate # On macOS/Linux
    # .\.venv\Scripts\activate # On Windows

    # Install all required libraries
    uv pip install -r requirements.txt
    ```
    The `requirements.txt` file contains:
    ```
    langchain
    langgraph
    langchain-core
    langchain-community
    python-dotenv
    langchain-openai
    langchain-groq
    arxiv
    wikipedia
    langgraph-cli[inmem]
    chromadb
    ipykernel
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of your project and add your API keys:

    ```dotenv
    OPENAI_API_KEY="your_openai_api_key_here"
    LANGCHAIN_API_KEY="your_langchain_api_key_here" # Optional, for Langsmith
    LANGCHAIN_TRACING_V2="true" # Enable Langsmith tracing
    LANGCHAIN_PROJECT="OpenAI-Agent-Demo" # Your Langsmith project name
    ```
    **Important:** Add `.env` to your `.gitignore` file to prevent accidentally committing your secrets.

## Usage

You can run the `openai_agent.py` script directly or integrate its `make_alternative_graph()` function into a Jupyter notebook for interactive testing.

```bash
# Example of running the agent from another Python script or interactive session
python -c "from openai_agent import agent; from langchain_core.messages import HumanMessage; print(agent.invoke({'messages': [HumanMessage(content='What is 2 + 2?')]}))"