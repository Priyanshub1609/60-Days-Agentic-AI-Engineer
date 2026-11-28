import ollama
from datetime import datetime

def calculator(a: float, b: float, operation: str):
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        return "Error: Cannot divide by zero" if b == 0 else a / b
    return "Invalid operation"

def get_datetime():
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

knowledge_base = {
    "agentic ai": "Agentic AI refers to AI systems that can plan, make decisions, use tools and execute tasks.",
    "python": "Python is a high-level programming language widely used in AI, automation and data science.",
    "llm": "A Large Language Model is an AI model trained to understand and generate human language."
}

def search_knowledge(topic: str):
    topic = topic.lower()
    for key, value in knowledge_base.items():
        if key in topic or topic in key:
            return value
    return "No information found in the local knowledge base."

tools = [
    {"type": "function", "function": {
        "name": "calculator", "description": "Perform mathematical calculations",
        "parameters": {"type": "object", "properties": {
            "a": {"type": "number"}, "b": {"type": "number"},
            "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]}
        }, "required": ["a", "b", "operation"]}
    }},
    {"type": "function", "function": {
        "name": "get_datetime", "description": "Get current date and time",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    {"type": "function", "function": {
        "name": "search_knowledge", "description": "Search information in the local knowledge base",
        "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}
    }}
]

def execute_tool(tool_name, arguments):
    if tool_name == "calculator":
        return calculator(arguments["a"], arguments["b"], arguments["operation"])
    if tool_name == "get_datetime":
        return get_datetime()
    if tool_name == "search_knowledge":
        return search_knowledge(arguments["topic"])
    return "Unknown tool"

conversation_history = []
SYSTEM_PROMPT = """
You are a helpful AI assistant.
You can use the available tools when necessary.
Remember the previous messages in this conversation.
Understand follow-up questions using conversation history.
Never invent tool results.
"""

def run_agent(user_input):
    global conversation_history
    if not conversation_history:
        conversation_history.append({"role": "system", "content": SYSTEM_PROMPT})
    conversation_history.append({"role": "user", "content": user_input})

    for step in range(5):
        print(f"\nAgent iteration: {step + 1}")
        response = ollama.chat(model="qwen2.5:3b", messages=conversation_history, tools=tools)
        conversation_history.append(response.message)
        tool_calls = response.message.tool_calls or []
        if not tool_calls:
            print("\nAI Agent:", response.message.content)
            return

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments
            print("\nTool selected:", tool_name)
            try:
                result = execute_tool(tool_name, arguments)
            except Exception as error:
                result = f"Tool error: {error}"
            print("Tool result:", result)
            conversation_history.append({"role": "tool", "tool_name": tool_name, "content": str(result)})

    print("\nMaximum iterations reached.")

if __name__ == "__main__":
    print("================================")
    print("    MEMORY ENABLED AI AGENT")
    print("================================")
    print("Type 'exit' to stop.")
    print("Type 'clear' to reset conversation memory.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("AI Agent: Goodbye!")
            break
        if user_input.lower() == "clear":
            conversation_history.clear()
            print("AI Agent: Conversation memory cleared.")
            continue
        if not user_input:
            continue
        try:
            run_agent(user_input)
        except Exception as error:
            print("\nError:", error)
