
from backend.routers import upload, chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. List the origins you want to allow. For dev you can use ["*"], but
#    in production you should list only your actual frontend domain(s).
origins = [
    "http://localhost:3000",           # your local dev site
    "https://www.embagent.com",      # your production site
    # add more as needed
]

# 2. Add the CORS middleware BEFORE you include your routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # or ["*"] during quick testing
    allow_credentials=True,
    allow_methods=["*"],               # GET, POST, PUT, etc.
    allow_headers=["*"],               # allow Authorization, Content-Type, etc.
)

# 3. Now include your existing routers
from backend.routers import chat   # or however you import it
app.include_router(chat.router, prefix="/chat")
# … any other routers …
@app.get("/")
def home():
    return {"msg": "Embagent API running"}