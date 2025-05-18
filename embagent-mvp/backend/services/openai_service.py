from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bot_intro(text, usecase):
    prompt = f"""You are an AI chatbot built for the following use case: {usecase}.
Here is the information provided to help you understand the domain:\n\n{text}\n\n
Respond with a short introductory message the bot might say when a user first interacts with it."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating bot response: {str(e)}"