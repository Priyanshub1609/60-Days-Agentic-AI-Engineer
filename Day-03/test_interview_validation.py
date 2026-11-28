from ai_interview_agent import InterviewPreparation
from pydantic import ValidationError

valid_data = {
    "job_role": "Data Analyst",
    "technical_skills": ["Python", "SQL"],
    "technical_questions": ["Explain SQL joins"],
    "hr_questions": ["Tell me about yourself"],
    "important_topics": ["Pandas", "Power BI"],
    "preparation_plan": ["Study SQL for 2 hours"]
}

result = InterviewPreparation(**valid_data)

invalid_data = valid_data.copy()
invalid_data["technical_skills"] = ["Python", "   "]
try:
    InterviewPreparation(**invalid_data)
    print("TEST FAILED")
except ValidationError:
    print("TEST PASSED: Empty skill rejected")

invalid_data = valid_data.copy()
invalid_data["salary"] = "5 LPA"
try:
    InterviewPreparation(**invalid_data)
    print("TEST FAILED")
except ValidationError:
    print("TEST PASSED: Extra field rejected")

invalid_data = valid_data.copy()
del invalid_data["job_role"]
try:
    InterviewPreparation(**invalid_data)
    print("TEST FAILED")
except ValidationError:
    print("TEST PASSED: Missing field rejected")

print(result)
