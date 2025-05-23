from fastapi import APIRouter, Request
from openai import OpenAI
from pydantic import BaseModel

router = APIRouter()
client = OpenAI()

class ChatInput(BaseModel):
    message: str
    icon: str
    name: str
    mission: str
    knowledge: str
    expertise: str
    etiquette: str
    links: str

@router.post("/chat")
async def chat(input: ChatInput):
    # 🔧 Construct a full system prompt on every message
    system_prompt = f"""
    You are a helpful AI assistant named {input.name}.

    Mission: {input.mission}
    Domain Expertise: {input.expertise}
    Tone: {input.etiquette}
    Reference Links: {input.links}

    Knowledge Base:
    {input.knowledge}

    Please respond helpfully and clearly using only the information above. Do not mention that you're an AI. Stay in character and remain consistent with your tone and mission.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input.message}
        ],
        temperature=0.7,
    )

    return {"response": response.choices[0].message.content.strip()}