from fastapi import APIRouter, Request
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    icon: str
    name: str
    mission: str
    knowledge: str
    expertise: str
    etiquette: str
    links: str

@router.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    prompt = f\"""
You are an expert AI assistant named {payload.name}.

Mission: {payload.mission}
Expertise: {payload.expertise}
Tone: {payload.etiquette}
Links (for reference): {payload.links}

Use only the following internal knowledge to answer the user's question:
\"\"\"
{payload.knowledge}
\"\"\"

Only answer questions using the above knowledge. Do not make assumptions or provide generic advice outside this data. 
If unsure, say: "Sorry, this request is outside of my scope of knowledge!".

User: {payload.message}
\"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are {payload.name}, a helpful domain expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
"""

# Save the updated file
chat_py_file_path = "/mnt/data/embagent_openai_api/embagent_openai_api/backend/routers/chat.py"
with open(chat_py_file_path, "w") as f:
    f.write(updated_chat_py)

chat_py_file_path  # Returning path for confirmation