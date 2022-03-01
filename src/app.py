from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils import router, TimeoutMiddleware
from .config import settings


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")
app.include_router(router, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TimeoutMiddleware)

@app.get("/ping")
def pong():
    return "Pong"
