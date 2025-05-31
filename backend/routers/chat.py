# backend/routers/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    icon: str
    name: str
    mission: str
    knowledge: str        # this is the text extracted from uploaded files
    expertise: str
    etiquette: str
    links: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # (1) Combine all the user's agent info into a system prompt
    system_prompt = f"""
    You are an AI assistant “{req.name}” specialized in {req.expertise or "general"}.
    Mission: {req.mission}
    Tone: {req.etiquette}
    Links: {req.links or "None"}
    Knowledge: {req.knowledge or "No additional knowledge."}
    Respond ONLY using the information from “Knowledge” (or “Links” if provided).
    If you must use logic, do so only to interpret that provided knowledge.
    Do NOT hallucinate details beyond the provided files or links.
    """
    user_message = req.message

    # (2) Build the messages list for the OpenAI chat completion
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        # Replace `openai` with however you have imported/configured it
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ai_response = completion.choices[0].message.content.strip()
        return {"response": ai_response}
    except Exception as e:
        # Log or re-raise as HTTPException
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")