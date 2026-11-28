import ollama
import json
from pydantic import BaseModel, ValidationError
from typing import Literal

class Task(BaseModel):
    task: str
    priority: Literal["High", "Medium", "Low"]
    deadline: str
    status: Literal["Pending", "Completed"]

prompt_template = """
You are an intelligent AI Task Planning Agent.

Analyze the user's request and extract task information.
Return ONLY valid JSON with these fields:
- task
- priority (High, Medium, Low)
- deadline
- status (Pending or Completed)

User Request: {user_task}
"""

user_task = input("\nWhat task do you want to plan? ")
final_prompt = prompt_template.format(user_task=user_task)

print("\nAI is analyzing your task...\n")
response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": final_prompt}],
    format="json"
)

try:
    result = json.loads(response["message"]["content"])
    validated_task = Task(**result)

    print("=" * 40)
    print("       AI TASK PLANNER")
    print("=" * 40)
    print("Task:", validated_task.task)
    print("Priority:", validated_task.priority)
    print("Deadline:", validated_task.deadline)
    print("Status:", validated_task.status)
    print("=" * 40)
    print("\nValidated JSON:")
    print(validated_task.model_dump_json(indent=4))

except json.JSONDecodeError:
    print("Invalid JSON returned by AI.")
except ValidationError as e:
    print("Task validation failed:")
    print(e)
except ollama.ResponseError as e:
    print("Ollama model error:", e)
except Exception as e:
    print("Unexpected error:", e)
