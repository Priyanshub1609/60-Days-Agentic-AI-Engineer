import ollama

prompt_template = """
You are an expert AI Task planning Assistant.

Your job is to undersatand the user's task
and provide a clear, actionable respoense.

User task: {task}

Instructions:
1. understand the task.
2. break it into smaller steps.
3. assign a priority.
4. keep the response practical.
"""

user_task = "I want to learn python in 30 days."
final_prompt = prompt_template.format(task=user_task)

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": final_prompt}]
)

print("\n==== AI TASK PLAN ====\n")
print(response["message"]["content"])
