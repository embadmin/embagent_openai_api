# backend/routers/upload.py
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
    """
    1. Read each uploaded file as UTF-8 text.
    2. Combine them (you can change this logic—e.g. do preprocessing here if needed).
    3. Return a JSON object containing the merged 'knowledgeText'.
    """
    try:
        # Read all file contents
        texts = []
        for f in files:
            raw = await f.read()                # bytes
            text = raw.decode("utf-8", "ignore")  # decode to string
            texts.append(text)

        # Combine into one giant knowledgeText
        knowledgeText = "\n\n".join(texts)

        # You might also want to save 'usecase', 'expertise', 'etiquette', 'links'
        # to a database or in-memory store here so that /chat can access them later.
        #
        # For now, we just return the concatenated text so the client can proceed.
        return { "knowledgeText": knowledgeText }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")