const API_BASE = "http://127.0.0.1:8000";

document.getElementById("find-contest-btn").addEventListener("click", async () => {
  const id = document.getElementById("contest-id-input").value;
  const errorEl = document.getElementById("cf-error");
  const resultEl = document.getElementById("cf-result");

  errorEl.textContent = "";
  resultEl.innerHTML = "";

  if (!id) {
    errorEl.textContent = "Введите ID контеста";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/codeforces?contest_id=${id}`);
    const data = await res.json();

    if (!res.ok) {
      errorEl.textContent = data.detail || "Ошибка";
      return;
    }

    const c = data.data;

    const start = new Date(c.startTimeSeconds * 1000);

    resultEl.innerHTML = `
      <div class="result">
        <div><b>Название:</b> ${c.name}</div>
        <div><b>Тип:</b> ${c.type}</div>
        <div><b>Фаза:</b> ${c.phase}</div>
        <div><b>Начало:</b> ${start.toLocaleString()}</div>
      </div>
    `;
  } catch {
    errorEl.textContent = "Не удалось подключиться к серверу";
  }
});
