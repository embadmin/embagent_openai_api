from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# === import your routers from the backend package ===
from backend.routers.upload import router as upload_router
from backend.routers.chat   import router as chat_router

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://<your-vercel-domain>.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Mount the routers
app.include_router(upload_router, prefix="")   # POST /upload
app.include_router(chat_router,   prefix="")   # POST /chat
@app.get("/")
def home():
    return {"msg": "Embagent API running"}