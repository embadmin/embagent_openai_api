from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import upload, chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit to frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(upload.router)
app.include_router(chat.router)  
@app.get("/")
def home():
    return {"msg": "Embagent API running"}