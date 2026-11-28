import json
from ai_interview_agent import InterviewPreparation, validate_ai_response

attempt_count = 0

def fake_ai_response():
    global attempt_count
    attempt_count += 1
    print(f"Fake AI attempt: {attempt_count}")

    if attempt_count < 3:
        return "INVALID JSON"

    return json.dumps({
        "job_role": "Data Analyst",
        "technical_skills": ["Python", "SQL"],
        "technical_questions": ["Explain SQL joins"],
        "hr_questions": ["Tell me about yourself"],
        "important_topics": ["Pandas", "Power BI"],
        "preparation_plan": ["Practice SQL daily"]
    })

def test_retry():
    for attempt in range(3):
        response = fake_ai_response()
        result = validate_ai_response(response)
        if result is not None:
            return result
    return None

result = test_retry()
print("\n===== TEST REPORT =====")
print("Total attempts:", attempt_count)

if result is not None and attempt_count == 3:
    print("TEST PASSED!")
    print("Agent recovered after two failures.")
else:
    print("TEST FAILED!")
