import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

API_BASE = "http://127.0.0.1:8000"

phase_map = {
    "FINISHED": "Завершенный",
    "BEFORE": "Будущий",
    "CODING": "Идет сейчас"
}

# ------------------------
# Статический градиент
# ------------------------
class GradientFrame(tk.Canvas):
    def __init__(self, parent, colors, **kwargs):
        super().__init__(parent, **kwargs)
        self.colors = colors  # [(R,G,B), (R,G,B)]
        self.height = kwargs.get("height", 600)
        self.width = kwargs.get("width", 480)
        self.draw_gradient()

    def draw_gradient(self):
        for i in range(self.height):
            t = i / self.height
            r = int(self.colors[0][0] + (self.colors[1][0] - self.colors[0][0]) * t)
            g = int(self.colors[0][1] + (self.colors[1][1] - self.colors[0][1]) * t)
            b = int(self.colors[0][2] + (self.colors[1][2] - self.colors[0][2]) * t)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(0, i, self.width, i, fill=color)

# ------------------------
# GUI
# ------------------------
root = tk.Tk()
root.title("Codeforces Contest Analytics")
root.geometry("480x600")
root.resizable(False, False)

# Статический градиент
colors = [(95, 114, 255), (66, 230, 149)]
bg_canvas = GradientFrame(root, colors, width=480, height=600)
bg_canvas.pack(fill="both", expand=True)

# Контейнер
container_bg = "#5f72ff"
container = tk.Frame(bg_canvas, bg=container_bg, padx=10, pady=10)
container.place(relx=0.5, rely=0.02, anchor="n")

# Заголовок
title_label = tk.Label(container, text="Codeforces Contest Analytics",
                       fg="white", bg=container_bg, font=("Segoe UI", 18, "bold"))
title_label.pack(pady=10)

# Карточка
card_bg = "#ffffff"  # теперь белая, без прозрачности
card = tk.Frame(container, bg=card_bg, bd=0, relief="ridge", padx=20, pady=20)
card.pack(pady=10, fill="x")

# Форма
tk.Label(card, text="Фаза контеста", bg=card_bg, fg="black", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0,5))
phase_var = tk.StringVar()
phase_menu = ttk.Combobox(card, textvariable=phase_var, values=["", "FINISHED", "BEFORE", "CODING"])
phase_menu.pack(fill="x", pady=(0,5))
phase_menu.set("")

tk.Label(card, text="Тип контеста", bg=card_bg, fg="black", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,0))
type_var = tk.StringVar()
type_menu = ttk.Combobox(card, textvariable=type_var, values=["", "CF", "ICPC"])
type_menu.pack(fill="x", pady=(0,5))
type_menu.set("")

tk.Label(card, text="Длительность (мин)", bg=card_bg, fg="black", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,0))
duration_frame = tk.Frame(card, bg=card_bg)
duration_frame.pack(fill="x", pady=5)
min_duration_var = tk.StringVar()
max_duration_var = tk.StringVar()
tk.Entry(duration_frame, textvariable=min_duration_var).pack(side="left", expand=True, fill="x", padx=(0,5))
tk.Entry(duration_frame, textvariable=max_duration_var).pack(side="left", expand=True, fill="x", padx=(5,0))

# Ошибка и статистика
error_label = tk.Label(card, text="", fg="#ff0000", bg=card_bg, font=("Segoe UI", 10, "bold"))
error_label.pack(pady=5)
stats_label = tk.Label(card, text="", fg="black", bg=card_bg, font=("Segoe UI", 10))
stats_label.pack(pady=5)

# Результаты
def create_result_frame():
    global result_frame
    result_frame = tk.Frame(card, bg=card_bg)
    result_frame.pack(fill="x", pady=5)
create_result_frame()

# ------------------------
# Функция загрузки контестов
# ------------------------
def load_contests():
    phase = phase_var.get()
    contest_type = type_var.get()
    min_d = min_duration_var.get()
    max_d = max_duration_var.get()

    error_label.config(text="")
    stats_label.config(text="")
    result_frame.destroy()
    create_result_frame()

    params = {}
    if phase: params["phase"] = phase
    if contest_type: params["contest_type"] = contest_type
    if min_d: params["min_duration"] = min_d
    if max_d: params["max_duration"] = max_d

    try:
        res = requests.get(f"{API_BASE}/codeforces/contests", params=params)
        res.raise_for_status()
        data = res.json()

        stats_label.config(text=f"Найдено контестов: {data['stats']['total']}\n"
                                f"Средняя длительность: {data['stats']['avg_duration']} мин")

        contests = data["contests"]
        if not contests:
            tk.Label(result_frame, text="Контесты не найдены по заданным фильтрам",
                     fg="black", bg=card_bg, font=("Segoe UI", 10)).pack(pady=5)
            return

        tk.Label(result_frame, text="🏆 Топ-3 последних контеста",
                 fg="black", bg=card_bg, font=("Segoe UI", 11, "bold")).pack(pady=(5,10))

        for idx, c in enumerate(contests, start=1):
            date = datetime.fromisoformat(c["startTime"])
            date_str = date.strftime("%d.%m.%Y")
            text = f"{idx}️⃣ {c['name']}\n{c['type']} • {phase_map.get(c['phase'], c['phase'])} • {date_str} • {c['durationMinutes']} мин"
            tk.Label(result_frame, text=text, fg="black", bg=card_bg,
                     font=("Segoe UI", 10), justify="left").pack(anchor="w", pady=2)

    except requests.RequestException as e:
        error_label.config(text="Ошибка при загрузке данных")
        print(e)

# Кнопка
load_btn = tk.Button(card, text="Показать контесты", command=load_contests,
                     bg="#e6e6ff", fg="#333", font=("Segoe UI", 10, "bold"))
load_btn.pack(pady=10, fill="x")

# ------------------------
# Запуск GUI
# ------------------------
root.mainloop()
