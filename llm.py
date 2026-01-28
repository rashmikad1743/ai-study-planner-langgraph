import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.5
)

def explain_topic(topic: str) -> str:
    prompt = f"""
    Explain the topic '{topic}' in very simple, student-friendly language.
    Give a short explanation and key points.
    """
    response = llm.invoke(prompt)
    return response.content
