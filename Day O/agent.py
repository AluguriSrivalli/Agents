import json
from datetime import datetime, UTC

# --- Tool implementations ---
def get_time(timezone: str = "UTC") -> str:
    # Use timezone-aware UTC datetime
    return f"Current UTC time is {datetime.now(UTC).isoformat(timespec='seconds')}"

def get_weather(city: str) -> str:
    fake = {"san francisco": "62F and foggy", "tehran": "78F and sunny"}
    return fake.get(city.lower(), f"weather for {city}: 70F and clear (fake)")

TOOLS_SPEC = {
    "get_weather": {
        "description": "Get the current weather for a real geographic city.",
        "parameters": ["city"],
    },
    "get_time": {
        "description": "Get the current time in UTC.",
        "parameters": ["timezone"],
    },
}

TOOL_IMPLS = {"get_weather": get_weather, "get_time": get_time}

# --- Agent loop ---
def run_agent(user_goal: str, max_steps: int = 6) -> str:
    messages = [
        {"role": "system", "content": "You are a terse assistant."},
        {"role": "user", "content": user_goal},
    ]

    for step in range(max_steps):
        user_text = messages[-1]["content"].lower()

        # Simple rule-based tool calling
        if "weather" in user_text:
            # Extract city name (naive approach)
            words = user_text.split()
            city = words[-1] if len(words) > 1 else "unknown"
            result = get_weather(city)
            messages.append({"role": "tool", "name": "get_weather", "content": result})
            return result

        elif "time" in user_text or "clock" in user_text:
            result = get_time()
            messages.append({"role": "tool", "name": "get_time", "content": result})
            return result

        else:
            # No tool match → just echo back
            return f"[assistant] I don’t know how to handle: {user_text}"

    return "[agent] hit max_steps without a final answer"


# --- Interactive loop ---
def main():
    print("Welcome to the tool‑using agent. Type 'quit' to exit.")
    while True:
        user_goal = input("Enter your request: ")
        if user_goal.lower() in {"quit", "exit"}:
            break
        answer = run_agent(user_goal)
        print("Agent:", answer)


if __name__ == "__main__":
    main()