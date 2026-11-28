# Day 02 — Tool Calling and Agent Memory

Day 02 extends a basic LLM chat loop into an agent that can call Python tools and retain conversation context.

## Concepts
- Function/tool schemas
- Tool dispatching and execution
- Calculator, date/time, and local knowledge-base tools
- Short-term conversation memory
- Bounded agent execution loops

## Projects

### `agent_with_tools.py`
A memory-enabled agent that can select and execute a calculator, date/time, or knowledge-base tool.

Run:
```bash
python agent_with_tools.py
```

### `personal_ai_assistant.py`
A more complete interactive assistant with tool execution, conversation memory, clear-memory and statistics commands.

Run:
```bash
python personal_ai_assistant.py
```

## Requirements
- Python 3.10+
- Ollama installed and running
- Model: `qwen2.5:3b`

Install:
```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
```

Run the scripts from this directory. The programs use the local Ollama service.
