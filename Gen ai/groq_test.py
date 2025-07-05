import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")  # ✅ Reads from your .env file
)

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "WAP TO GENERATE A STAR WITH TRIANGLE"}
    ],
    model="llama3-70b-8192"
)

print(chat_completion.choices[0].message.content)
