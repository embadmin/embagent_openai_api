from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
import os
from PyPDF2 import PdfReader
import docx
from openai import OpenAI



router = APIRouter()
client = OpenAI()

async def extract_text_from_file(file: UploadFile) -> str:
    try:
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

        elif filename.endswith((".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".c", ".ts")):
            return content.decode("utf-8")

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            return f"[Image file uploaded: {file.filename}]"

        else:
            return f"[Unsupported file type: {file.filename}. This type is not supported yet — but coming soon!]"

    except Exception as e:
        return f"[Error reading {file.filename}: {str(e)}]"

@router.post("/upload")
async def upload_file(
    files: Optional[List[UploadFile]] = File(None),
    usecase: str = Form(...),
    expertise: str = Form(""),
    etiquette: str = Form(""),
    links: str = Form("")
):
    try:
        all_text = ""
        if files:
            for file in files:
                text = await extract_text_from_file(file)
                all_text += f"\n\n---\n{file.filename}\n{text}"
        else:
            all_text = "[No files uploaded]"

        prompt = f"""
        You are a helpful AI agent with the following context:
        Use Case: {usecase}
        Expertise: {expertise}
        Tone: {etiquette}
        Reference Links: {links}
        Knowledge Base: {all_text}
        Please first send an introduction message for yourself according to the tone and information provided. Only one introduction message is allowed.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        first_message = response.choices[0].message.content.strip()

        return {
            "received_files": [f.filename for f in files] if files else [],
            "usecase": usecase,
            "expertise": expertise,
            "etiquette": etiquette,
            "links": links,
            "bot_response": first_message
        }

    except Exception as e:
        print("❌ Upload error:", str(e))
        return {"error": str(e)}