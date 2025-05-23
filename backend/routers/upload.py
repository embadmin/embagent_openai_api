from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
import os
from PyPDF2 import PdfReader
import docx
from openai import OpenAI



router = APIRouter()
client = OpenAI()

# 🔹 File reader logic
async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return content.decode("utf-8")
    elif filename.endswith(".pdf"):
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)
        reader = PdfReader(temp_path)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif filename.endswith(".docx"):
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)
        doc = docx.Document(temp_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return f"[Unsupported file type: {file.filename}]"


@router.post("/upload")
async def upload_file(
    files: Optional[List[UploadFile]] = File(None),  # ✅ make optional
    usecase: str = Form(...),
    expertise: str = Form(...),
    etiquette: str = Form(...),
    links: str = Form(...)
):
    all_text = ""

    if files:
        for file in files:
            text = await extract_text_from_file(file)
            all_text += f"\n\n---\n{file.filename}\n{text}"
    else:
        all_text = "[No files uploaded]"

    prompt = f"""
You are a helpful AI agent with the following traits:

Use Case: {usecase}
Expertise: {expertise}
Tone: {etiquette}
Links provided: {links}

Base your answers only on the following knowledge:
{all_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return {
        "received_files": [f.filename for f in files],
        "usecase": usecase,
        "expertise": expertise,
        "etiquette": etiquette,
        "links": links
    }