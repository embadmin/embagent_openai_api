from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.routers import upload, chat

app = FastAPI()

# 🔁 1) HTTPS Redirect Middleware FIRST
# @app.middleware("http")
# async def redirect_to_https(request: Request, call_next):
#     # 👇 Check Render's forwarded protocol
#     forwarded_proto = request.headers.get("x-forwarded-proto")
#     if forwarded_proto == "http":
#         url = request.url.replace(scheme="https")
#         return RedirectResponse(url=str(url))
#     return await call_next(request)curl -I https://embagent-openai-api.onrender.com/upload
# 🔐 2) THEN apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.embagent.com"],
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