
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import router as api_router
from app.core.config import Config
from app.core.limiter import limiter

app = FastAPI(title="Portfolio RAG Chatbot")

# Add Limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
# Check if Config has CORS_ORIGINS, else default to all
origins = getattr(Config, "CORS_ORIGINS", ["*"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount data directory for file access (e.g. Resume)
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
if os.path.exists(data_dir):
    app.mount("/files", StaticFiles(directory=data_dir), name="files")

app.include_router(api_router)

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(static_dir, "index.html"))
