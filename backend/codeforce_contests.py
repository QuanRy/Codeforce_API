import requests
from fastapi import HTTPException

CODEFORCES_URL = "https://codeforces.com/api/contest.list"


def fetch_contests():
    response = requests.get(CODEFORCES_URL, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Codeforces API недоступен"
        )

    data = response.json()

    if data.get("status") != "OK":
        raise HTTPException(
            status_code=500,
            detail=data.get("comment", "Ошибка Codeforces API")
        )

    return data["result"]


def get_contest_by_id(contest_id: int):
    contests = fetch_contests()

    for contest in contests:
        if contest.get("id") == contest_id:
            return contest

    return None
