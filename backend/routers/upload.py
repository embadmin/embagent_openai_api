from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from backend.services.openai_service import generate_bot_intro
import fitz  # PyMuPDF for PDFs
import docx2txt
from PIL import Image
import io

router = APIRouter()

async def extract_text(upload_file: UploadFile) -> str:
    filename = upload_file.filename.lower()

    raw_bytes = await upload_file.read()

    if filename.endswith(".txt"):
        return raw_bytes.decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf"):
        try:
            doc = fitz.open(stream=raw_bytes, filetype="pdf")
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            raise HTTPException(400, f"Failed to read PDF: {str(e)}")

    elif filename.endswith(".docx"):
        with open(f"/tmp/{filename}", "wb") as f:
            f.write(raw_bytes)
        return docx2txt.process(f"/tmp/{filename}")

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        # Optionally integrate OCR here (placeholder for now)
        return f"[Image file {filename} uploaded]"

    else:
        return f"[Unsupported file type: {filename}]"

@router.post("/", summary="Upload knowledge files")
async def upload_files(
    files: List[UploadFile] = File(...),
    usecase: str            = Form(...),
    expertise: str          = Form(""),
    etiquette: str          = Form(""),
    links: str              = Form("")
):
    """
    Accept files, extract text, and generate agent intro via OpenAI.
    """
    try:
        all_text = [await extract_text(f) for f in files]
        combined_text = "\n\n".join(all_text)

        # 🔥 Use OpenAI to summarize & introduce
        knowledge_text = generate_bot_intro(combined_text, usecase)

        return {
            "filename_list": [f.filename for f in files],
            "knowledgeText": knowledge_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))