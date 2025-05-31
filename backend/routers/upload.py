# backend/routers/upload.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import textract  # or any library you use for extracting text from files

router = APIRouter()

@router.post("/", summary="Upload knowledge files")
async def upload_files(
    files: List[UploadFile] = File(...),
    usecase: str = Form(...),
    expertise: str = Form(""),
    etiquette: str = Form(""),
    links: str = Form(""),
):
    """
    1) Accept multiple files, extract text, and combine into one large string.
    2) Return that combined text so the front-end can store it as `knowledgeText`.
    """
    all_text = []
    for upload_file in files:
        try:
            # read file contents
            contents = await upload_file.read()
            # extract text (depending on file type)
            text = textract.process(upload_file.filename, input_data=contents).decode("utf-8")
            all_text.append(text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract {upload_file.filename}: {e}")

    combined = "\n\n".join(all_text).strip()
    return JSONResponse({
        "filename_list": [f.filename for f in files],
        "knowledgeText": combined
    })