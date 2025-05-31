# backend/routers/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()
client = OpenAI()

class ChatRequest(BaseModel):
    model: str
    messages: list[dict]
    temperature: float = 0.2

@router.post("/chat")
async def chat_with_agent(body: ChatRequest):
    """
    Simply forwards the `messages` array to OpenAI's ChatCompletion endpoint.
    """
    completion = await client.chat.completions.create(
        model=body.model,
        messages=body.messages,
        temperature=body.temperature
    )

    return {
        "response": completion.choices[0].message.content.strip()
    }