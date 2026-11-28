# Day 03 — Prompt Engineering, Structured Outputs, and Validation

Day 03 focuses on making agent responses more dependable by using clear prompts, JSON output, Pydantic schemas, input validation, and retry handling.

## Projects

| File | Purpose |
|---|---|
| `prompt_engineering.py` | Uses a reusable prompt template to ask an LLM for a practical task plan |
| `structured_output.py` | Requests JSON from Ollama and validates the result with Pydantic |
| `task_planner.py` | Interactive task planner with JSON parsing and schema validation |
| `ai_resume_analyzer.py` | Validates resume input and generates a structured resume analysis with retry handling |
| `ai_interview_agent.py` | Generates a structured interview preparation report from a job role and description |
| `test_retry.py` | Tests resume-analyzer retry behavior with a simulated Ollama response |
| `test_interview_validation.py` | Checks interview schema validation |
| `test_interview_retry.py` | Exercises a simulated invalid-then-valid response sequence |

## Setup

- Python 3.10+
- Ollama installed and running
- Model: `qwen2.5:3b`

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
```

## Run projects

```bash
python prompt_engineering.py
python structured_output.py
python task_planner.py
python ai_resume_analyzer.py
python ai_interview_agent.py
```

## Run validation and retry exercises

```bash
python test_interview_validation.py
python test_retry.py
python test_interview_retry.py
```

Run commands from the `Day-03` directory. The AI projects require the local Ollama service and the specified model. The test scripts use simulated responses where applicable and do not require live model generation for those test paths.
