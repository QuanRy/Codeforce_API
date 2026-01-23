from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.codeforce_contests import router as contests_router

app = FastAPI(
    title="Codeforces Analytics API",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contests_router)
