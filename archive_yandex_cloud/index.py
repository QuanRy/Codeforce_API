import json
import requests
import pandas as pd 

CODEFORCES_URL = "https://codeforces.com/api/contest.list"

def get_contests_df() -> pd.DataFrame:
    """Загрузка контестов и подготовка DataFrame"""
    r = requests.get(CODEFORCES_URL, timeout=10)
    if r.status_code != 200:
        raise Exception("Ошибка Codeforces API")
    
    data = r.json()
    if data.get("status") != "OK":
        raise Exception(data.get("comment", "Ошибка CF"))
    
    df = pd.DataFrame(data["result"])
    df["startTime"] = pd.to_datetime(df["startTimeSeconds"], unit="s", errors="coerce")
    df["durationMinutes"] = df["durationSeconds"] // 60
    return df

def handler(event, context):
    """
    Облачная функция Yandex.Cloud для аналитики Codeforces.
    GET-параметры: phase, contest_type, min_duration, max_duration
    Возвращает JSON с stats и топ-3 последних контестов.
    """
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "OK"})
        }

    query = event.get("queryStringParameters") or {}
    phase = query.get("phase")
    contest_type = query.get("contest_type")
    min_duration = query.get("min_duration")
    max_duration = query.get("max_duration")

    try:
        min_duration = int(min_duration) if min_duration is not None else None
    except:
        min_duration = None
    try:
        max_duration = int(max_duration) if max_duration is not None else None
    except:
        max_duration = None

    try:
        df = get_contests_df()

        if phase:
            df = df[df["phase"] == phase.upper()]
        if contest_type:
            df = df[df["type"] == contest_type.upper()]
        if min_duration is not None:
            df = df[df["durationMinutes"] >= min_duration]
        if max_duration is not None:
            df = df[df["durationMinutes"] <= max_duration]

        stats = {
            "total": int(len(df)),
            "avg_duration": round(df["durationMinutes"].mean(), 1) if not df.empty else 0
        }

        contests = df.sort_values("startTime", ascending=False).head(3)
        contests_json = contests[["name", "type", "phase", "durationMinutes", "startTime"]].to_dict(orient="records")

        body = {"stats": stats, "contests": contests_json}
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(body, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
