from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()
client = OpenAI()

# Temporary in-memory chat histories (reset on server restart)
chat_histories = {}

class ChatInput(BaseModel):
    session_id: str  # unique ID to track conversation
    message: str
    icon: str
    name: str
    mission: str
    expertise: str
    etiquette: str
    links: str

@router.post("/chat")
async def chat(input: ChatInput):
    system_prompt = f"""
You are an AI assistant named {input.name}.
Mission: {input.mission}
Expertise: {input.expertise}
Tone: {input.etiquette}
Reference: {input.links}

Be helpful and respond based on prior messages in this session.
"""

    # Start or update session history
    history = chat_histories.get(input.session_id, [])
    if not history:
        history.append({"role": "system", "content": system_prompt})

    history.append({"role": "user", "content": input.message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        temperature=0.7,
    )

    bot_reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": bot_reply})
    chat_histories[input.session_id] = history  # save for next round

    return {"response": bot_reply}