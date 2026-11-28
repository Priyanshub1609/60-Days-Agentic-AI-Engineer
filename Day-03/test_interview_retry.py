import json
from ai_interview_agent import generate_with_retry

attempt_count = 0

def fake_ollama_chat(**kwargs):
    global attempt_count
    attempt_count += 1
    print(f"Fake model attempt: {attempt_count}")

    if attempt_count < 3:
        return {"message": {"content": "INVALID JSON"}}

    valid_response = {
        "job_role": "Data Analyst",
        "technical_skills": ["Python", "SQL"],
        "technical_questions": ["Explain SQL joins"],
        "hr_questions": ["Tell me about yourself"],
        "important_topics": ["Pandas", "Power BI"],
        "preparation_plan": ["Practice SQL daily"]
    }
    return {"message": {"content": json.dumps(valid_response)}}

result = generate_with_retry(
    prompt="Test interview preparation",
    max_retries=3,
    chat_fn=fake_ollama_chat
)

print("\n===== TEST REPORT =====")
print("Expected attempts: 3")
print("Actual attempts:", attempt_count)

if result is not None and attempt_count == 3:
    print("TEST PASSED!")
    print("The real retry function recovered after two invalid responses.")
else:
    print("TEST FAILED!")
