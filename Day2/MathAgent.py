import re,getpass
import os
import json
import sys
from typing import Any
from groq import Groq

##Implementing tool calls
def add(a:float, b:float) -> float:
  return a+b

def subtract(a:float, b:float) -> float:
  return a-b

def multiply(a:float, b:float) -> float:
  return a*b

def exponent(a:float, b:float) -> float:
  return a**b

def division(a:float, b:float) -> float:
  return a/b

##Tools implements
TOOL_IMPLS: dict[str, Any] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "exponent": exponent,
    "division": division,
}

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Addition of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                    "b": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                },
                "required": ["a","b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Addition of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                    "b": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                },
                "required": ["a","b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Addition of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                    "b": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                },
                "required": ["a","b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "division",
            "description": "Addition of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                    "b": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                },
                "required": ["a","b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "exponent",
            "description": "Addition of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                    "b": {"type": "number", "description": "It has to be a number either an interger or a float. ex:2, 5.8"},
                },
                "required": ["a","b"],
                "additionalProperties": False,
            },
        },
    },
]

def call_tool_with_retry(name, args, max_retries=2):
    impl = TOOL_IMPLS.get(name)
    if impl is None:
        return json.dumps({"ok": False, "error": f"Unknown tool: {name}"})

    for attempt in range(max_retries + 1):
        try:
            result = impl(**args)
            return json.dumps({"ok": True, "data": result})
        except Exception as exc:
            if attempt == max_retries:
                return json.dumps({"ok": False, "error": f"Tool crashed after {max_retries+1} tries: {exc}"})
    return json.dumps({"ok": False, "error": "Unexpected retry exhaustion"})

SYSTEM_PROMPT = """\
You are a precise, concise assistant with access to tools.

## Reasoning protocol (ReAct style)
Before every tool call, write one short "Thought:" line explaining WHY you need it.
After receiving a tool result, write one short "Observation:" line summarising what you learned.

## Tool policy
- The user's request may contain multiple sub-questions. Do not produce a final answer until every sub-question has been either answered (via a tool or your own knowledge) or explicitly flagged as unsupported.
- Call a tool only when it directly answers a sub-question.
- Factual questions you already know: answer from knowledge (use tools for arithmetic).
- Never invent arguments a tool was not designed for.

## Confidence gate (F)
When you are ready to give the final answer, first output:
  Confidence: <HIGH|MEDIUM|LOW> — <one-sentence reason>
Then give the actual answer.

## Style
Be terse. Bullet-points over prose. No filler phrases.
"""
def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and paste your key."
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Main agent loop
# ---------------------------------------------------------------------------

def run_agent(user_goal: str, max_steps: int = 10) -> str:
    client = get_client()
    import os
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_goal},
    ]

    print(f"\n{'='*60}")
    print(f"USER: {user_goal}")
    print(f"{'='*60}")

    for step in range(max_steps):

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS_SPEC,
            tool_choice="auto",
            temperature=0.2,
        )
        msg = resp.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))

        # ---- No tool calls → final answer (with streaming simulation) --------
        if not msg.tool_calls:
            content = msg.content or ""

            # G. Stream final answer character-by-character
            print(f"\n[final answer @ step {step}]")
            for char in content:
                print(char, end="", flush=True)
            print()
            return content

        # ---- Tool calls -------------------------------------------------------
        print(f"\n[step {step}] — {len(msg.tool_calls)} tool call(s):")
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            print(f"  -> {name}({json.dumps(args)})")

            # D. call with retry
            result_str = call_tool_with_retry(name, args,max_retries=5)
            result_data = json.loads(result_str)

            status = "ok" if result_data.get("ok") else "ERR"
            print(f"     [{status}] {result_data.get('data') or result_data.get('error')}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": result_str,
                }
            )

    return "[agent] hit max_steps without a final answer"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    goal = (
            "What's the weather in Paris and Berlin? "
            "what is sum of 8 and 15 "
            "Then calculate the average of 65 and 55. "
            "Finally, summarise everything."
            )
    run_agent(goal)
