from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.codeforce_contests import get_contest_by_id

app = FastAPI(
    title="Codeforces Contest Finder",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/codeforces")
def find_contest(
    contest_id: int = Query(..., ge=1, description="ID контеста Codeforces")
):
    contest = get_contest_by_id(contest_id)

    if contest is None:
        raise HTTPException(
            status_code=404,
            detail=f"Контест с ID {contest_id} не найден"
        )

    return {
        "status": "ok",
        "data": contest
    }
