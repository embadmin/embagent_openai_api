from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_agent(
    files: List[UploadFile] = File(...),
    usecase: str        = Form(...),
    expertise: str      = Form(...),
    etiquette: str      = Form(...),
    links: str          = Form(""),
):
    try:
        texts = []
        for f in files:
            data = await f.read()
            texts.append(data.decode("utf-8", "ignore"))
        knowledgeText = "\n\n".join(texts)
        return { "knowledgeText": knowledgeText }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))