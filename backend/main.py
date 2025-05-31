# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import upload, chat

app = FastAPI()

# 1) Allow CORS from your frontend origin (http://localhost:3000 or your domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.embagent.com"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],        # allows GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],        # allows any request headers
)

# 2) Then include your routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
@app.get("/")
def home():
    return {"msg": "Embagent API running"}