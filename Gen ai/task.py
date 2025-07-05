import os
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai

# loading environment variables and having api keyss
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Initialize Groq SDK client
groq_client = Groq(api_key=GROQ_API_KEY)

# Groq API Call (Domain Expert) 
def call_groq(prompt, system_prompt="You are a domain expert."):
    chat_completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

# Gemini API Call (Critic) 
def call_gemini(prompt, system_prompt="You are a critical reviewer."):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    full_prompt = f"{system_prompt}\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text
#to check whether it is a new ques or user just want to get check the answer again
def is_followup_or_critique(user_input):
    followups = [
        "is that correct", "are you sure", "can you verify", 
        "was that right", "check that", "is it true", 
        "is that right", "really?", "hmm?", "not sure"
    ]
    return any(phrase in user_input.lower() for phrase in followups)


# Main Chat Loop 
def run_chat_agent():
    print("Multi-Agent Chatbot (type 'exit' or 'quit' to stop)\n")

    last_groq_response = ""
    last_user_question = ""
    
    while True:
        user_input = input("[USER] ")

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        #saving api call 
        if not user_input.strip():
            print("Please enter something.")
            continue


        if last_groq_response and is_followup_or_critique(user_input):
            critic_prompt = (
                f"The user previously asked: \"{last_user_question}\" "
                f"and the expert replied: \"{last_groq_response}\". "
                f"The user now says: \"{user_input}\". "
                f"Please verify or critique the expert's answer."
            )
            critic_response = call_gemini(critic_prompt)
            print(f"[GEMINI CRITIC] {critic_response}")
        else:
            expert_response = call_groq(user_input)
            print(f"[GROQ AGENT] {expert_response}")
            last_groq_response = expert_response
            last_user_question = user_input



if __name__ == "__main__":
    run_chat_agent()
