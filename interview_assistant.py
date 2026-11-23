import ollama

MODEL = "llama3.2"


# ==========================================
# 1. SELECT INTERVIEW DIFFICULTY
# ==========================================

print("\nSelect Interview Difficulty")
print("1. Beginner")
print("2. Intermediate")
print("3. Advanced")

choice = input("Enter your choice (1-3): ")

if choice == "1":
    difficulty = "Beginner"

elif choice == "2":
    difficulty = "Intermediate"

elif choice == "3":
    difficulty = "Advanced"

else:
    difficulty = "Beginner"
    print("Invalid choice. Beginner selected by default.")

print(f"\nSelected Level: {difficulty}")


# ==========================================
# 2. SYSTEM PROMPT
# ==========================================

system_prompt = f"""
You are an expert technical interviewer
specializing in Data Analyst interviews.

Candidate difficulty level: {difficulty}

Difficulty guidelines:

BEGINNER:
Ask fundamental questions about SQL,
Python, Excel, statistics, and data analysis.

INTERMEDIATE:
Ask practical scenario-based questions,
SQL queries, data cleaning, and analytical problems.

ADVANCED:
Ask complex business problems,
optimization, advanced SQL, statistics,
and analytical case studies.

For every candidate answer:

1. Evaluate technical accuracy from 1 to 10.
2. Evaluate clarity from 1 to 10.
3. Evaluate practical understanding from 1 to 10.
4. Evaluate communication from 1 to 10.
5. Give an overall score.
6. Explain strengths.
7. Explain areas of improvement.
8. Provide an ideal answer.
9. Ask one follow-up question.

Ask one question at a time.
Be supportive but honest.
"""


# ==========================================
# 3. INITIALIZE CONVERSATION
# ==========================================

messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]

print("\n🤖 AI Interview Assistant")
print("-" * 40)

question_count = 0


# ==========================================
# 4. MAIN CHAT LOOP
# ==========================================

while True:

    user_input = input("\nYou: ").strip()

    # Exit command
    if user_input.lower() == "exit":

        print("\nAI: Thank you for attending the interview!")
        print(f"Total interactions: {question_count}")

        break


    # Reset command
    elif user_input.lower() == "reset":

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        question_count = 0

        print("\nAI: Interview restarted!")

        continue


    # Help command
    elif user_input.lower() == "help":

        print("""
Available Commands:

exit  - Exit the interview
reset - Restart the interview
help  - Show commands
""")

        continue


    # Ignore empty input
    elif user_input == "":

        print("Please enter something.")

        continue


    # ==========================================
    # 5. ADD USER MESSAGE
    # ==========================================

    messages.append({
        "role": "user",
        "content": user_input
    })


    # ==========================================
    # 6. CALL OLLAMA
    # ==========================================

    try:

        response = ollama.chat(
            model=MODEL,
            messages=messages
        )

        assistant_reply = response["message"]["content"]


    except Exception as e:

        print(f"\nError communicating with Ollama: {e}")

        # Remove failed user message from history
        messages.pop()

        continue


    # ==========================================
    # 7. DISPLAY AI RESPONSE
    # ==========================================

    print("\nAI:", assistant_reply)


    # ==========================================
    # 8. UPDATE COUNTER
    # ==========================================

    question_count += 1

    print(f"\nInteractions completed: {question_count}")


    # ==========================================
    # 9. SAVE AI RESPONSE IN HISTORY
    # ==========================================

    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })