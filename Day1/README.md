# 🧑‍💻 Build a ReAct AI Agent from Scratch in Python

This project demonstrates how to implement the **ReAct pattern** (Reasoning + Acting) using pure Python, simple tools, and an agent loop — without relying on frameworks like LangChain or LlamaIndex.

---

## 🚀 What You’ll Learn
- Understand the **ReAct agent pattern**:
  - **Reasoning**: the agent thinks step by step.
  - **Acting**: the agent calls tools to gather information.
  - **Observing**: the agent incorporates tool results back into reasoning.
- Implement an agent loop without external frameworks.
- Connect an LLM (or simple rule‑based logic) to custom tools.
- Build a foundation for more advanced AI agents.

---

## 📦 Requirements
- Python 3.9+
- Standard libraries: `json`, `datetime`
- (Optional) An LLM API client (OpenAI, Groq, Hugging Face) if you want to connect to real models.

Install dependencies if you plan to use external APIs:
```bash
pip install openai huggingface_hub groq
