import ollama
import json
from pydantic import BaseModel
from typing import Literal

prompt = """
You are an AI task extraction assistant.

Extract the user's task into JSON.

Return ONLY valid JSON using this structure:

{
    "task": "task description",
    "priority": "High, Medium, or Low",
    "deadline": "deadline",
    "status": "Pending"
}

User request:
I want to complete my Python project by tomorrow.
"""

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}],
    format="json"
)

result = json.loads(response["message"]["content"])

print("\n===== STRUCTURED TASK =====")
print(json.dumps(result, indent=4))
print("\nTask:", result["task"])
print("Priority:", result["priority"])
print("Deadline:", result["deadline"])

class Task(BaseModel):
    task: str
    priority: Literal["High", "Medium", "Low"]
    deadline: str
    status: Literal["Pending", "Completed"]

validated_task = Task(**result)

print("\n===== PYDANTIC VALIDATION =====")
print(validated_task)
print("\nTask:", validated_task.task)
print("\nPriority:", validated_task.priority)
print("\nStatus:", validated_task.status)
