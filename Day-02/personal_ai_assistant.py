import ollama
from datetime import datetime

MODEL_NAME = "qwen2.5:3b"
MAX_ITERATIONS = 5

SYSTEM_PROMPT = """
You are a helpful personal AI assistant.
Available tools: calculator, date/time, and local knowledge base.
Use tools when appropriate, remember conversation history, and never invent tool results.
"""

def calculator(a: float, b: float, operation: str):
    if operation == "add": return a + b
    if operation == "subtract": return a - b
    if operation == "multiply": return a * b
    if operation == "divide": return "Error: Cannot divide by zero" if b == 0 else a / b
    return "Invalid operation"

def get_datetime():
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

knowledge_base = {
    "agentic ai": "Agentic AI refers to AI systems that can plan, make decisions, use tools and execute tasks.",
    "python": "Python is a high-level programming language widely used in AI, automation and data science.",
    "llm": "A Large Language Model is an AI model trained to understand and generate human language.",
    "machine learning": "Machine Learning is a branch of AI that enables computers to learn patterns from data.",
    "api": "An API allows different software applications to communicate with each other.",
    "automation": "Automation uses technology to perform tasks with reduced manual intervention."
}

def search_knowledge(topic: str):
    topic = topic.lower().strip()
    for key, value in knowledge_base.items():
        if key in topic or topic in key:
            return value
    return "No information found in the local knowledge base."

tools = [
    {"type": "function", "function": {
        "name": "calculator", "description": "Perform mathematical calculations.",
        "parameters": {"type": "object", "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"},
            "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]}
        }, "required": ["a", "b", "operation"]}
    }},
    {"type": "function", "function": {
        "name": "get_datetime", "description": "Get current local date and time.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    {"type": "function", "function": {
        "name": "search_knowledge", "description": "Search information in the local knowledge base.",
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
    return "Unknown tool requested."

agent_state = {
    "conversation_history": [],
    "user_name": None,
    "running": True,
    "tool_calls": 0
}

def initialize_memory():
    if not agent_state["conversation_history"]:
        agent_state["conversation_history"].append({"role": "system", "content": SYSTEM_PROMPT})

def save_message(message):
    agent_state["conversation_history"].append(message)

def clear_memory():
    agent_state["conversation_history"].clear()
    agent_state["user_name"] = None
    print("\nAssistant: Conversation memory cleared.")

def run_agent(user_input):
    initialize_memory()
    history = agent_state["conversation_history"]
    save_message({"role": "user", "content": user_input})

    for step in range(MAX_ITERATIONS):
        print(f"\n[Agent Iteration: {step + 1}]")
        response = ollama.chat(model=MODEL_NAME, messages=history, tools=tools)
        save_message(response.message)
        tool_calls = response.message.tool_calls or []

        if not tool_calls:
            print("\nAI Assistant:")
            print(response.message.content)
            return

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments
            print("\nSelected Tool:", tool_name)
            print("Arguments:", arguments)
            try:
                result = execute_tool(tool_name, arguments)
            except Exception as error:
                result = f"Tool execution error: {error}"
            agent_state["tool_calls"] += 1
            print("Tool Result:", result)
            save_message({"role": "tool", "tool_name": tool_name, "content": str(result)})

    print("\nAgent stopped: Maximum iterations reached.")

def show_stats():
    print("\n========== AGENT STATISTICS ==========")
    print("Total tool calls:", agent_state["tool_calls"])
    print("Messages stored:", len(agent_state["conversation_history"]))
    print("User name:", agent_state["user_name"])
    print("======================================")

def main():
    print("\n" + "=" * 45)
    print("       PERSONAL AI ASSISTANT")
    print("=" * 45)
    print("\nAvailable commands:")
    print("1. clear  - Clear conversation memory")
    print("2. stats  - Show agent statistics")
    print("3. exit   - Close assistant")
    print("\nStart chatting with your AI assistant!")

    while agent_state["running"]:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        command = user_input.lower()
        if command in ["exit", "quit", "bye"]:
            agent_state["running"] = False
            print("\nAssistant: Goodbye!")
            break
        if command == "clear":
            clear_memory()
            continue
        if command == "stats":
            show_stats()
            continue
        try:
            run_agent(user_input)
        except Exception as error:
            print("\nApplication Error:", error)

if __name__ == "__main__":
    main()
