import json
import ollama
from typing import List
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

def validate_user_input(job_role, job_description):
    return bool(job_role.strip()) and len(job_description.strip()) >= 50

class InterviewPreparation(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    job_role: str = Field(min_length=1)
    technical_skills: List[str]
    technical_questions: List[str]
    hr_questions: List[str]
    important_topics: List[str]
    preparation_plan: List[str]

    @field_validator("technical_skills", "technical_questions", "hr_questions", "important_topics", "preparation_plan")
    @classmethod
    def validate_list_items(cls, values):
        for item in values:
            if not item.strip():
                raise ValueError("List items cannot be empty")
        return values

def create_interview_prompt(job_role, job_description):
    return f"""
You are an expert technical interviewer and career coach.
Target Job Role:
{job_role}

Job Description:
{job_description}

Generate technical skills, technical interview questions, HR questions,
important topics, and a practical preparation plan.

Rules:
- Focus on the supplied job description.
- Do not invent requirements.
- Return structured JSON only, matching the required schema.
"""

def generate_interview_preparation(prompt, chat_fn=None):
    if chat_fn is None:
        chat_fn = ollama.chat
    response = chat_fn(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}],
        format=InterviewPreparation.model_json_schema()
    )
    return response["message"]["content"]

def validate_ai_response(ai_response):
    try:
        result = json.loads(ai_response)
        validated_result = InterviewPreparation(**result)
        print("\nAI response validation successful!")
        return validated_result
    except json.JSONDecodeError as error:
        print("\nInvalid JSON response:", error)
        return None
    except ValidationError as error:
        print("\nPydantic validation failed:", error)
        return None

def generate_with_retry(prompt, max_retries=3, chat_fn=None):
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries}")
        try:
            ai_response = generate_interview_preparation(prompt, chat_fn=chat_fn)
            validated_result = validate_ai_response(ai_response)
            if validated_result is not None:
                print("\nInterview preparation successful!")
                return validated_result
            print("Invalid response. Retrying...")
        except ollama.ResponseError as error:
            print("Ollama error:", error)
            return None
        except Exception as error:
            print("Unexpected error:", error)
            if attempt == max_retries - 1:
                return None
    print("\nMaximum retries reached.")
    return None

def display_interview_report(result):
    print("\n========== INTERVIEW PREPARATION REPORT ==========")
    print("\nJob Role:", result.job_role)
    for title, values in [
        ("Technical Skills", result.technical_skills),
        ("Technical Questions", result.technical_questions),
        ("HR Questions", result.hr_questions),
        ("Important Topics", result.important_topics),
        ("Preparation Plan", result.preparation_plan)
    ]:
        print(f"\n{title}:")
        for value in values:
            print("-", value)
    print("\n========== JSON OUTPUT ==========")
    print(result.model_dump_json(indent=4))

def main():
    print("\n===== AI INTERVIEW PREPARATION AGENT =====")
    job_role = input("\nEnter your target job role: ")
    job_description = input("\nPaste the job description: ")

    if not validate_user_input(job_role, job_description):
        print("\nInvalid input! Enter a job role and a job description of at least 50 characters.")
        return

    print("\nInput validation successful!")
    prompt = create_interview_prompt(job_role, job_description)
    print("\nGenerating interview preparation...")
    result = generate_with_retry(prompt, max_retries=3)

    if result is not None:
        display_interview_report(result)
    else:
        print("\nInterview preparation failed.")

if __name__ == "__main__":
    main()
