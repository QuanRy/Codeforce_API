import requests
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/codeforces", tags=["Codeforces"])

CODEFORCES_URL = "https://codeforces.com/api/contest.list"


def get_contests_df() -> pd.DataFrame:
    r = requests.get(CODEFORCES_URL)
    if r.status_code != 200:
        raise HTTPException(500, "Ошибка Codeforces API")

    data = r.json()
    if data.get("status") != "OK":
        raise HTTPException(500, data.get("comment", "Ошибка CF"))

    df = pd.DataFrame(data["result"])
    df["startTime"] = pd.to_datetime(df["startTimeSeconds"], unit="s", errors="coerce")
    df["durationMinutes"] = df["durationSeconds"] // 60
    return df


@router.get("/contests")
def contests_analytics(
    phase: str | None = Query(None, description="FINISHED / BEFORE / CODING"),
    contest_type: str | None = Query(None, description="CF / ICPC / IOI"),
    min_duration: int | None = Query(None, description="Мин. длительность (мин)"),
    max_duration: int | None = Query(None, description="Макс. длительность (мин)")
):
    df = get_contests_df()

    if phase:
        df = df[df["phase"] == phase.upper()]
    if contest_type:
        df = df[df["type"] == contest_type.upper()]
    if min_duration:
        df = df[df["durationMinutes"] >= min_duration]
    if max_duration:
        df = df[df["durationMinutes"] <= max_duration]

    stats = {
        "total": int(len(df)),
        "avg_duration": round(df["durationMinutes"].mean(), 1) if not df.empty else 0,
        "by_type": df["type"].value_counts().to_dict()
    }

    contests = df.sort_values("startTime", ascending=False).head(15)

    return {
        "stats": stats,
        "contests": contests[
            ["name", "type", "phase", "durationMinutes", "startTime"]
        ].to_dict(orient="records")
    }
