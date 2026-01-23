import requests
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/codeforces", tags=["Codeforces"])

CODEFORCES_URL = "https://codeforces.com/api/contest.list"


def get_contests_df() -> pd.DataFrame:
    """
    Загружает список контестов Codeforces и преобразует в DataFrame
    """
    r = requests.get(CODEFORCES_URL, timeout=10)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка Codeforces API")

    data = r.json()
    if data.get("status") != "OK":
        raise HTTPException(status_code=500, detail=data.get("comment", "Ошибка CF"))

    df = pd.DataFrame(data["result"])

    # нормализация данных
    df["startTime"] = pd.to_datetime(
        df["startTimeSeconds"], unit="s", errors="coerce"
    )
    df["durationMinutes"] = df["durationSeconds"] // 60

    return df


@router.get("/contests")
def contests_analytics(
    phase: str | None = Query(None, description="FINISHED / BEFORE / CODING"),
    contest_type: str | None = Query(None, description="CF / ICPC / IOI"),
    min_duration: int | None = Query(None, description="Мин. длительность (мин)"),
    max_duration: int | None = Query(None, description="Макс. длительность (мин)")
):
    """
    Аналитика контестов Codeforces с фильтрами
    """
    df = get_contests_df()

    # --- фильтрация ---
    if phase:
        df = df[df["phase"] == phase.upper()]

    if contest_type:
        df = df[df["type"] == contest_type.upper()]

    if min_duration is not None:
        df = df[df["durationMinutes"] >= min_duration]

    if max_duration is not None:
        df = df[df["durationMinutes"] <= max_duration]

    # --- аналитика ---
    stats = {
        "total": int(len(df)),
        "avg_duration": round(df["durationMinutes"].mean(), 1)
        if not df.empty else 0
    }

    # --- берём ТОЛЬКО 3 последних контеста ---
    contests = (
        df.sort_values("startTime", ascending=False)
          .head(3)
    )

    return {
        "stats": stats,
        "contests": contests[
            ["name", "type", "phase", "durationMinutes", "startTime"]
        ].to_dict(orient="records")
    }
