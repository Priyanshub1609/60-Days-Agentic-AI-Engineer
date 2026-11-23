import ollama
from datetime import datetime

# =========================
# 1. SYSTEM PROMPT
# =========================

system_prompt = """
You are an intelligent AI assistant.

Your rules:
1. Give clear, accurate, and helpful answers.
2. Explain complex topics in simple language.
3. Remember relevant information from the conversation.
4. If you don't know something, admit it.
5. When explaining code, provide practical examples.
6. Keep answers concise unless detailed explanation is requested.
7. Ask clarifying questions when the user's request is unclear.
8. Never invent facts or pretend to have performed actions.
"""


# =========================
# 2. INITIALIZE MEMORY
# =========================

def initialize_messages():
    return [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


messages = initialize_messages()



# =========================
# 3. CHAT FUNCTION
# =========================

def chat_with_ai(user_input):

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=messages
        )

        assistant_response = response["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        return assistant_response

    except Exception as e:

        messages.pop()

        return f"AI Error: {e}"


# =========================
# 4. HISTORY FUNCTION
# =========================

def display_history():

    message_count = 0

    print("\n========== CHAT HISTORY ==========\n")

    for message in messages:

        if message["role"] == "system":
            continue

        role = message["role"].upper()
        content = message["content"]

        print(f"{role}: {content}\n")

    print("================================\n")

def save_history():
    filename = f'chat_history_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt'
    try:
        with open(filename,'w',encoding='utf-8') as file:
            file.write("AI ASSISTANT - CoNVERSATION HISTORY\n")
            file.write('='*40 +"\n\n")

            for message in messages:
                if message['role'] == 'system':
                    continue
                role = message['role'].upper()
                content = message['content']

                file.write(f'{role}:{content}\n\n')

        print(f"\nConversation saved successfully : {filename}\n")
    except Exception as e:
        print(f"\nError saving conversatiom : {e}\n")



# =========================
# 5. MAIN APPLICATION
# =========================

def main():
    message_count = 0

    print("=" * 40)
    print("       AI ASSISTANT V3")
    print("=" * 40)

    print("Commands: exit | clear | history | save")
    print("AI Model: llama3.2:3b\n")

    while True:

        user_input = input("You: ").strip()

        # Exit
        if user_input.lower() == "exit":
            print("\nAI: Goodbye! Have a great day.")
            break

        # Ignore empty input
        if not user_input:
            continue

        # Clear conversation
        if user_input.lower() == "clear":
            global messages
            messages = initialize_messages()

            message_count = 0

            print("\nAI: Conversation history cleared!")
            print("Message counter reset!\n")
            continue

        # Display history
        if user_input.lower() == "history":
            display_history()
            continue

        # Save history
        if user_input.lower() == "save":
            save_history()
            continue

        # Chat with AI
        response = chat_with_ai(user_input)

        if not response.startswith("AI Error:"):
            message_count += 1

        print(f"\nAI: {response}\n")
        print(f"Messages exchanged: {message_count}\n")


if __name__ == "__main__":
    main()