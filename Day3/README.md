# Fundamentals of LangChain

## Overview

LangChain is a powerful framework for building applications powered by language models. At its core, an **Agent** consists of two key components:

- **Model**: The underlying language model (e.g., GPT-4, Claude)
- **Harness**: The complete framework around the model loop, including prompts, tools, and middleware that control behavior

*This guide is based on the [LangChain Official Documentation](https://python.langchain.com/).*

---

## Getting Started with LangChain

### Installation

To get started with LangChain, install it in your Python environment using pip:

```bash
pip install -U langchain
```

The `-U` flag ensures you install the latest version of LangChain.

---

## Environment Setup

### ⚠️ Important: Store API Keys as Environment Variables

To connect your agent to a language model API (such as OpenAI, Google Generative AI, or others), you need to securely store your API key as an **environment variable**:

1. **Create a `.env` file** in your project root
2. **Add your API key** to the file:

```
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

3. **Load the environment variables** in your Python code:

```python
from dotenv import load_dotenv
load_dotenv()
```

This uses the `load_dotenv` function from the `python-dotenv` package to read your `.env` file and load environment variables into your application.

**⚡ Best Practice**: Never hardcode API keys in your source code. Always use environment variables to keep your credentials secure.

---

## Creating Your First Agent

### Basic Agent Structure

To create an agent, import the `create_agent` function from LangChain:

```python
from langchain.agents import create_agent
```

### Agent Initialization

Here's how to initialize a basic agent:

```python
agent = create_agent(
    model="openai:gpt-4",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
```

### Parameters Explained

| Parameter | Description |
|-----------|-------------|
| `model` | Specifies the language model to use (e.g., `"openai:gpt-4"`, `"openai:gpt-3.5-turbo"`, `"gemini-3.1-flash-lite"`) |
| `tools` | A list of functions that the agent can call to perform specific tasks |
| `system_prompt` | Defines the agent's role and behavior (e.g., "You are a helpful assistant") |

---

## Understanding `create_agent` vs `create_deep_agent`

### `create_agent`

`create_agent` is a standard agent constructor from LangChain that creates a basic agentic loop. It:

- **Executes a single pass** through the agent loop
- Uses the language model to decide which tool to call
- Returns the result after the model responds
- Best for **simple, single-turn interactions** or straightforward tasks
- Lower computational overhead and faster response times

**Use Case**: When you need quick answers or simple tool invocations without complex reasoning chains.

```python
agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Your question here"}]},
    config={"configurable": {"thread_id": "session-id"}},
)
```

### `create_deep_agent`

`create_deep_agent` (from the `deepagents` package) creates an **advanced multi-step reasoning agent**. It:

- **Supports iterative reasoning** with multiple agent loops
- Can perform **complex multi-step reasoning** and planning
- Remembers context across multiple tool invocations
- Can handle **complex queries** that require breaking down into sub-tasks
- Provides **deeper analysis** of problems before deciding on actions
- Better for **research-intensive tasks** and problems requiring deliberate reasoning

**Use Case**: When you need the agent to think through complex problems, perform multiple research steps, or analyze data from multiple sources before providing an answer.

```python
deep_agent = create_deep_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

result = deep_agent.invoke(
    {"messages": [{"role": "user", "content": "Your complex question here"}]},
    config={"configurable": {"thread_id": "session-id"}},
)
```

### Quick Comparison

| Feature | `create_agent` | `create_deep_agent` |
|---------|----------------|-------------------|
| **Reasoning Depth** | Single pass | Multi-step iterative |
| **Complexity** | Simple tasks | Complex tasks |
| **Speed** | Faster | Slower (more thorough) |
| **Context Memory** | Limited | Extended across steps |
| **Use Case** | Quick answers | Deep research/analysis |
| **Overhead** | Low | High |

---

## Example: Weather Tool

```python
def get_weather(location: str) -> str:
    """Fetch weather information for a given location."""
    # Implementation details
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(
    model="openai:gpt-4",
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant",
)
```

---

## Built-in Agent Examples

### Basic Agent

The `basicAgent.py` file demonstrates a simple agent implementation with:
- Basic model initialization
- Tool integration
- Simple system prompts

### Research Agent

The `researchAgent.py` file contains an advanced agent that demonstrates:
- **Comparison** of `create_agent` and `create_deep_agent` 
- Fetching and analyzing text data from URLs
- Processing complex queries requiring tool invocation
- Using `InMemorySaver` for checkpointing agent state
- Multi-step reasoning with different agent types

This demonstrates how agents can be extended with custom tools to work with your specific use case and how different agent creation strategies impact task performance.

---

## Key Concepts

1. **Model Agnostic**: LangChain supports multiple language model providers
2. **Tool Integration**: Agents can be equipped with custom functions (tools) to extend their capabilities
3. **Configurable**: The `create_agent` function allows fine-grained control over agent behavior
4. **Flexible Prompting**: The `system_prompt` parameter shapes how the agent responds
5. **Harness-Driven**: All the infrastructure around the model (prompts, tools, middleware) is what makes agents powerful
6. **Multi-step Reasoning**: Use `create_deep_agent` for complex tasks requiring iterative reasoning

---

## Next Steps

- Explore the `basicAgent.py` file for a complete working example
- Check out `researchAgent.py` to see how to compare `create_agent` and `create_deep_agent`
- Refer to the [LangChain Official Documentation](https://python.langchain.com/) for more advanced features
- Experiment with different tools and prompts to customize your agent's behavior

---

## Resources

- [LangChain Official Documentation](https://python.langchain.com/)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)
- [Python-dotenv Package](https://pypi.org/project/python-dotenv/)
- [LangGraph for Agent State Management](https://python.langchain.com/docs/langgraph/)
