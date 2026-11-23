import ollama

# Configuration
MODEL_NAME = "llama3.2"

# Ask user for subject
subject = input("Enter the subject you want to study: ")

print("\nChoose your learning mode:")
print("1. Explain a Topic")
print("2. Quiz Mode")
print("3. Practical Examples")

mode_choice = input("Enter your choice (1/2/3): ")

# Select learning mode
if mode_choice == "1":
    learning_mode = "Explain a Topic"
    mode_instruction = """
    Explain concepts in simple language.
    Use step-by-step explanations.
    Give examples whenever necessary.
    """

elif mode_choice == "2":
    learning_mode = "Quiz Mode"
    mode_instruction = """
    Act as an interactive quiz teacher.
    Ask one question at a time.
    Wait for the student's answer.
    Evaluate the answer.
    Explain the correct answer.
    Give the next question.
    """

elif mode_choice == "3":
    learning_mode = "Practical Examples"
    mode_instruction = """
    Teach using practical examples.
    Provide real-world use cases.
    Include code examples whenever appropriate.
    Explain the code step by step.
    """

else:
    print("Invalid choice. Defaulting to Explain Mode.")
    learning_mode = "Explain a Topic"
    mode_instruction = """
    Explain concepts in simple language.
    Use step-by-step explanations.
    Give examples whenever necessary.
    """

# Create system prompt
system_prompt = f"""
You are an intelligent AI Study Assistant.

Student's subject: {subject}
Learning mode: {learning_mode}

Your responsibilities:
- Teach the student clearly.
- Keep explanations beginner-friendly.
- Encourage the student to think.
- Avoid unnecessary complicated theory.
- Provide examples.

Learning instructions:
{mode_instruction}
"""

# Initialize conversation history
messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]

interaction_count = 0

print("\n" + "=" * 50)
print("AI STUDY ASSISTANT STARTED")
print("=" * 50)

print(f"Subject: {subject}")
print(f"Learning Mode: {learning_mode}")

print("\nCommands:")
print("exit  - Exit the assistant")
print("reset - Reset conversation")
print("help  - Show commands")

print("=" * 50)

# Main conversation loop
while True:

    user_input = input("\nYou: ").strip()

    # Handle empty input
    if not user_input:
        print("Please enter something.")
        continue

    # Exit command
    if user_input.lower() == "exit":
        print("\nGoodbye! Happy learning.")
        break

    # Help command
    elif user_input.lower() == "help":
        print("\nAvailable commands:")
        print("exit  - Exit the assistant")
        print("reset - Reset conversation")
        print("help  - Show commands")
        continue

    # Reset command
    elif user_input.lower() == "reset":

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        interaction_count = 0

        print("Conversation has been reset.")
        continue

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        # Call Ollama
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )

        assistant_response = response["message"]["content"]

        # Add AI response to history
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        interaction_count += 1

        print("\nAI Study Assistant:")
        print(assistant_response)

        print(f"\nInteractions: {interaction_count}")

    except Exception as error:

        print("\nSomething went wrong!")
        print("Error:", error)

        # Remove failed user message
        messages.pop()