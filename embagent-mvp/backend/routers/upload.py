from fastapi import APIRouter, UploadFile, File, Form
from backend.services.openai_service import generate_bot_intro

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), usecase: str = Form(...)):
    content = await file.read()
    file_text = content.decode("utf-8")

    response = generate_bot_intro(file_text, usecase)
    return {"bot_response": response}