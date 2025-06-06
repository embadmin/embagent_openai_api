# ─────────────────────────────────────────────────────────────────────────
# backend/routers/upload.py
# ─────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing  import List

router = APIRouter()

@router.post("/", summary="Upload knowledge files")
async def upload_files(
    files: List[UploadFile] = File(...),
    usecase: str            = Form(...),
    expertise: str          = Form(""),
    etiquette: str          = Form(""),
    links: str              = Form(""),
):
    """
    
    1) Accept multiple UploadFile objects.
    2) Read each upload as raw bytes, decode as UTF-8 (for plain .txt).
    3) Return combined text under 'knowledgeText'.
    """

    all_text = []
    for upload_file in files:
        try:
            # Read the file's raw bytes
            raw_bytes = await upload_file.read()
            # Decode as UTF-8 (ignoring any non-UTF8 sequences)
            text = raw_bytes.decode("utf-8", errors="ignore")
            all_text.append(text)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not process `{upload_file.filename}`: {str(e)}"
            )

    combined_text = "\n\n".join(all_text).strip()

    return {
        "filename_list":   [f.filename for f in files],
        "knowledgeText":   combined_text
    }