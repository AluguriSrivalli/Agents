# Fundamentals of LangChain

## Overview

LangChain is a powerful framework for building applications powered by language models. At its core, an **Agent** consists of two key components:

- **Model**: The underlying language model (e.g., GPT-4, Claude)
- **Harness**: The complete framework around the model loop, including prompts, tools, and middleware that control behavior

*This guide is based on the LangChain Official Documentation.*

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

To connect your agent to a language model API (such as OpenAI), you need to set up your API key:

1. **Create a `.env` file** in your project root
2. **Add your API key** to the file:

```
OPENAI_API_KEY=your_api_key_here
```

3. **Load the environment variables** in your Python code:

```python
from dotenv import load_dotenv
load_dotenv()
```

This uses the `load_dotenv` function from the `python-dotenv` package to read your `.env` file and load environment variables into your application.

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
| `model` | Specifies the language model to use (e.g., `"openai:gpt-4"`, `"openai:gpt-3.5-turbo"`) |
| `tools` | A list of functions that the agent can call to perform specific tasks |
| `system_prompt` | Defines the agent's role and behavior (e.g., "You are a helpful assistant") |

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

The `researchAgent.py` file contains an advanced agent that can:
- Answer questions about your files
- Search and retrieve information from your documents
- Provide summarized insights based on your data

This demonstrates how agents can be extended with custom tools to work with your specific use case.

---

## Key Concepts

1. **Model Agnostic**: LangChain supports multiple language model providers
2. **Tool Integration**: Agents can be equipped with custom functions (tools) to extend their capabilities
3. **Configurable**: The `create_agent` function allows fine-grained control over agent behavior
4. **Flexible Prompting**: The `system_prompt` parameter shapes how the agent responds
5. **Harness-Driven**: All the infrastructure around the model (prompts, tools, middleware) is what makes agents powerful

---

## Next Steps

- Explore the `basicAgent.py` file for a complete working example
- Check out `researchAgent.py` to see how to build agents that interact with documents
- Refer to the [LangChain Official Documentation](https://python.langchain.com/) for more advanced features
- Experiment with different tools and prompts to customize your agent's behavior

---

## Resources

- [LangChain Official Documentation](https://python.langchain.com/)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)
- [Python-dotenv Package](https://pypi.org/project/python-dotenv/)
