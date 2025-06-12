from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from backend.routers import upload, chat

app = FastAPI()

# 🔁 1) HTTPS Redirect Middleware FIRST

@app.middleware("http")
async def reject_http(request: Request, call_next):
    proto = request.headers.get("x-forwarded-proto")
    if proto == "http":
        return JSONResponse(
            content={"error": "HTTPS only"},
            status_code=400
        )
    return await call_next(request)
# 🔐 2) THEN apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 3) Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def home():
    return {"msg": "Embagent API running"}