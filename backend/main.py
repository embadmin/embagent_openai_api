from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from routers.upload import router as upload_router
from routers.chat   import router as chat_router

app = FastAPI()

# === CORS setup ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "http://localhost:3000",
      "https://www.embagent.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Mount the upload and chat endpoints ===
app.include_router(upload_router, prefix="")   # handles POST /upload
app.include_router(chat_router,   prefix="")   # handles POST /chat
@app.get("/")
def home():
    return {"msg": "Embagent API running"}