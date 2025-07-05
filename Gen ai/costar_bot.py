from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.runnables import RunnableMap
from langchain_groq import ChatGroq
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

prompt = PromptTemplate.from_template("""
You are a product copywriting assistant.

Write a compelling product description in the CO-STAR format.

Context: {context}
Objective: {objective}
Style: {style}
Tone: {tone}
Audience: {audience}
Response: {response}

Your output must ONLY be in the following raw JSON format, with no explanations or extra text :
{{
  "headline": "...",
  "description": "..."
}}
""")

class ProductOutput(BaseModel):
    headline: str
    description: str

parser = PydanticOutputParser(pydantic_object=ProductOutput)

llm = ChatGroq(
    temperature=0.7,
    model_name="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY")  # ✅ Loaded securely from .env
)

parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

chain = prompt | llm | parser

input_data = {
    "context": "This is a smartwatch designed for fitness lovers.",
    "objective": "Highlight its health-tracking features to encourage purchases.",
    "style": "Crisp and modern",
    "tone": "Energetic and motivational",
    "audience": "Young professionals and athletes",
    "response": "Highlight the unique features that make it better than competitors."
}

result = chain.invoke(input_data)
print(result)
