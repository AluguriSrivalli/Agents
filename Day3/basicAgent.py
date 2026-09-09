from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Using the updated active model ID for Groq
agent = create_agent(
    model="groq:qwen/qwen3.6-27b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)

# Display the final response
print(result["messages"][-1].content)
