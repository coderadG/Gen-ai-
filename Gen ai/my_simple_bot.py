def run_chat_agent():
    print(" Hello! I'm your assistant.(SIMPLE BOT)")
    print("I'll ask you a few questions. Type 'exit' or 'quit' anytime to stop.\n")

    questions = [
        "What's your name?",
        "What are you currently studying or interested in?",
        "Do you have a favorite programming language?"
    ]

    for question in questions:
        user_input = input(f"[BOT] {question}\n[YOU] ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            return
        
        # Keyword-based reply logic
        response = ""
        input_lower = user_input.lower()
        
        if "python" in input_lower:
            response = " Python is great for both beginners and experts!"
        elif "java"in input_lower:
            response = "Java is a high-level, object-oriented programming language"
        elif "ai" in input_lower or "machine learning" in input_lower:
            response = " AI is transforming the world. Exciting choice!"
        elif "name" in question.lower():
            response = f"Nice to meet you, {user_input.strip()}!"
        else:
            response = "That's interesting!"

        print(f"[BOT] {response}\n")

    print(" That was fun! Have a great day ahead.")




if __name__ == "__main__":
    run_chat_agent()

