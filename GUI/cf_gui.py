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
# GUI
# ------------------------
root = tk.Tk()
root.title("Codeforces Contest Analytics")
root.geometry("480x720")  # +100 пикселей
root.resizable(False, False)
root.configure(bg="#5f72ff")

# ------------------------
# Контейнер
# ------------------------
container = tk.Frame(root, bg="#5f72ff")
container.pack(padx=10, pady=10, fill="both", expand=True)

# ------------------------
# Заголовок
# ------------------------
title_label = tk.Label(container, text="Codeforces Contest Analytics",
                       fg="white", bg="#5f72ff",
                       font=("Segoe UI", 20, "bold"))
title_label.pack(pady=(20, 10))

# ------------------------
# Карточка
# ------------------------
card_bg = "#e0e6f2"
card = tk.Frame(container, bg=card_bg, bd=0, relief="ridge")
card.pack(pady=10, fill="x", padx=10)

# ------------------------
# Стиль для ttk Combobox
style = ttk.Style()
style.theme_use('clam')
style.configure("Rounded.TCombobox",
                padding=5,
                relief="flat",
                font=("Segoe UI", 11),
                foreground="#2b2b2b",
                background="#ffffff",
                borderwidth=0)
style.map("Rounded.TCombobox",
          fieldbackground=[("readonly", "#ffffff")],
          background=[("readonly", "#ffffff")])

entry_bg = "#ffffff"
entry_font = ("Segoe UI", 11)

# ------------------------
# Функция для создания закруглённого Entry
def rounded_entry(parent, textvariable, width=None):
    frame = tk.Frame(parent, bg="#ffffff")
    frame.pack(side="left", fill="x", expand=True, padx=2)
    entry = tk.Entry(frame, textvariable=textvariable, bg="#ffffff", font=entry_font,
                     bd=0, relief="flat", highlightthickness=1, highlightbackground="#999999",
                     width=width)
    entry.pack(fill="x", ipady=6, padx=5)
    return entry

# ------------------------
# Форма
def create_label(frame, text):
    return tk.Label(frame, text=text, bg=card_bg, fg="#2b2b2b", font=("Segoe UI", 11, "bold"))

# Фаза
create_label(card, "Фаза контеста").pack(anchor="w", pady=(8,2))
phase_var = tk.StringVar()
phase_frame = tk.Frame(card, bg=card_bg)
phase_frame.pack(fill="x", padx=10, pady=(0,5))
phase_menu = ttk.Combobox(phase_frame, textvariable=phase_var,
                          values=["Любая", "Завершенный", "Будущий", "Идет сейчас"],
                          state="readonly", style="Rounded.TCombobox")
phase_menu.pack(fill="x", ipady=5)
phase_menu.set("Любая")

# Тип
create_label(card, "Тип контеста").pack(anchor="w", pady=(5,2))
type_var = tk.StringVar()
type_frame = tk.Frame(card, bg=card_bg)
type_frame.pack(fill="x", padx=10, pady=(0,5))
type_menu = ttk.Combobox(type_frame, textvariable=type_var,
                         values=["Любой", "CF", "ICPC"],
                         state="readonly", style="Rounded.TCombobox")
type_menu.pack(fill="x", ipady=5)
type_menu.set("Любой")

# Длительность
create_label(card, "Длительность (мин)").pack(anchor="w", pady=(5,2))
duration_frame = tk.Frame(card, bg=card_bg)
duration_frame.pack(fill="x", padx=10, pady=(0,5))
min_duration_var = tk.StringVar()
max_duration_var = tk.StringVar()
# Уменьшена ширина полей, чтобы влезли рядом
min_entry = rounded_entry(duration_frame, min_duration_var, width=10)
max_entry = rounded_entry(duration_frame, max_duration_var, width=10)

# Ошибка и статистика
error_label = tk.Label(card, text="", fg="#ff4d4d", bg=card_bg, font=("Segoe UI", 10, "bold"))
error_label.pack(pady=(5,2))
stats_label = tk.Label(card, text="", fg="#2b2b2b", bg=card_bg, font=("Segoe UI", 11))
stats_label.pack(pady=(0,5))

# ------------------------
# Результаты
def create_result_frame():
    global result_frame
    result_frame = tk.Frame(card, bg=card_bg)
    result_frame.pack(fill="x", pady=5)
create_result_frame()

# ------------------------
# Загрузка контестов
def load_contests():
    phase = phase_var.get()
    contest_type = type_var.get()
    min_d = min_duration_var.get()
    max_d = max_duration_var.get()

    error_label.config(text="")
    stats_label.config(text="")
    result_frame.destroy()
    create_result_frame()

    phase_map_api = {"Любая": "", "Завершенный":"FINISHED","Будущий":"BEFORE","Идет сейчас":"CODING"}
    type_map_api = {"Любой": "", "CF":"CF","ICPC":"ICPC"}

    params = {}
    if phase_map_api[phase]: params["phase"] = phase_map_api[phase]
    if type_map_api[contest_type]: params["contest_type"] = type_map_api[contest_type]
    if min_d: params["min_duration"] = min_d
    if max_d: params["max_duration"] = max_d

    try:
        res = requests.get(f"{API_BASE}/codeforces/contests", params=params)
        res.raise_for_status()
        data = res.json()

        stats_label.config(text=f"Найдено контестов: {data['stats']['total']} | "
                                f"Средняя длительность: {data['stats']['avg_duration']} мин")

        contests = data["contests"]
        if not contests:
            tk.Label(result_frame, text="Контесты не найдены по заданным фильтрам",
                     fg="#2b2b2b", bg=card_bg, font=("Segoe UI", 11)).pack(pady=5)
            return

        tk.Label(result_frame, text="Топ-3 последних контеста",
                 fg="#2b2b2b", bg=card_bg, font=("Segoe UI", 12, "bold")).pack(pady=(5,5))

        for idx, c in enumerate(contests, start=1):
            date = datetime.fromisoformat(c["startTime"])
            date_str = date.strftime("%d.%m.%Y")
            text = f"{idx}. {c['name']}\n{c['type']} • {phase_map.get(c['phase'], c['phase'])} • {date_str} • {c['durationMinutes']} мин"
            tk.Label(result_frame, text=text, fg="#2b2b2b", bg=card_bg,
                     font=("Segoe UI", 11), justify="left", anchor="w").pack(anchor="w", pady=1)

    except requests.RequestException as e:
        error_label.config(text="Ошибка при загрузке данных")
        print(e)

# ------------------------
# Кнопка
load_btn = tk.Button(card, text="Показать контесты", command=load_contests,
                     bg="#ffffff", fg="#333", font=("Segoe UI", 11, "bold"),
                     bd=0, relief="raised", padx=10, pady=8, activebackground="#e6e6ff")
load_btn.pack(pady=8, fill="x", padx=10)

# ------------------------
# Запуск GUI
root.mainloop()
