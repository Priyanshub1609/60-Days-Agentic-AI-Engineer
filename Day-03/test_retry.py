import json
import inspect
from ai_resume_analyzer import analyze_resume_with_retry

attempt_count = 0

def fake_ollama_chat(**kwargs):
    global attempt_count
    attempt_count += 1
    print(f"\nFAKE OLLAMA CALLED! Attempt: {attempt_count}")

    if attempt_count < 3:
        return {"message": {"content": "INVALID JSON RESPONSE"}}

    valid_response = {
        "candidate_level": "Fresher",
        "technical_skills": ["Python", "SQL"],
        "soft_skills": ["Communication"],
        "strengths": ["Problem solving"],
        "weaknesses": ["No professional experience"],
        "recommended_roles": ["Data Analyst"],
        "improvement_suggestions": ["Build more projects"]
    }
    return {"message": {"content": json.dumps(valid_response)}}

print("\n===== RETRY FUNCTION DIAGNOSTICS =====")
print("Function signature:", inspect.signature(analyze_resume_with_retry))
print("\n===== STARTING RETRY TEST =====")

result = analyze_resume_with_retry(
    prompt="Test resume",
    max_retries=3,
    chat_fn=fake_ollama_chat
)

print("\n===== RETRY TEST REPORT =====")
print("Expected attempts: 3")
print("Actual attempts:", attempt_count)

if result is not None and attempt_count == 3:
    print("\nTEST PASSED!")
    print("Agent recovered after two failures.")
    print("\nRecovered candidate level:")
    print(result.candidate_level)
else:
    print("\nTEST FAILED!")
