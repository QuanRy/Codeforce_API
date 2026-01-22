import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Codeforces Contest Finder",
    description="Найти контест Codeforces по ID. Примеры ID: 2170, 1950, 1881",
    version="1.0"
)

# --- Разрешаем CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CODEFORCES_URL = "https://codeforces.com/api/contest.list"

def fetch_contests_data():
    """Получает данные о контестах с Codeforces API"""
    response = requests.get(CODEFORCES_URL)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"HTTP ошибка: {response.status_code}")

    data = response.json()

    if data.get("status") != "OK":
        raise HTTPException(status_code=500, detail=data.get("comment", "Ошибка в API"))

    return data["result"]

@app.get("/")
def get_contest_by_id(contest_id: int = Query(..., description="Введите ID контеста (например: 2170, 1950, 1881)")):
    """Найти контест по ID"""
    contests = fetch_contests_data()
    
    # Ищем контест по ID
    contest = next((c for c in contests if c.get("id") == contest_id), None)
    
    if contest is None:
        raise HTTPException(status_code=404, detail=f"Контест с ID {contest_id} не найден")
    
    return {
        "message": "Контест найден",
        "contest_id": contest_id,
        "data": contest
    }