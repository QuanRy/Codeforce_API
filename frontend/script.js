// Базовый URL бэкенда
const API_BASE = "https://backend-web-api.onrender.com";
const API_CF = `${API_BASE}/codeforce_api`;

// === Codeforces: Найти контест по ID ===
document.getElementById("find-contest-btn").addEventListener("click", async () => {
  const id = parseInt(document.getElementById("contest-id-input").value.trim());
  const errorEl = document.getElementById("cf-error");
  const resultEl = document.getElementById("cf-result");

  errorEl.textContent = "";
  resultEl.innerHTML = "";

  // Проверка диапазона
  if (isNaN(id) || id < 1 || id > 2000) {
    errorEl.textContent = "Пожалуйста, введите ID в интервале 1–2000";
    return;
  }

  try {
    const res = await fetch(`${API_CF}/?contest_id=${id}`);
    const data = await res.json();

    if (data.error) {
      errorEl.textContent = data.error;
      return;
    }

    const c = data.data;

    // Длительность
    let duration = "";
    if (c.durationSeconds >= 3600) {
      const hours = Math.floor(c.durationSeconds / 3600);
      const minutes = Math.floor((c.durationSeconds % 3600) / 60);
      duration = `${hours} ч ${minutes} мин`;
    } else {
      const minutes = Math.floor(c.durationSeconds / 60);
      duration = `${minutes} мин`;
    }

    // Время начала
    const startDate = new Date(c.startTimeSeconds * 1000);
    const day = String(startDate.getDate()).padStart(2, "0");
    const month = String(startDate.getMonth() + 1).padStart(2, "0");
    const year = startDate.getFullYear();
    const hours = String(startDate.getHours()).padStart(2, "0");
    const minutes = String(startDate.getMinutes()).padStart(2, "0");

    resultEl.innerHTML = `
      <div class="cf-table">
        <div class="cf-row"><div class="cf-label-left">Название:</div><div class="cf-value">${c.name}</div></div>
        <div class="cf-row"><div class="cf-label-left">Тип:</div><div class="cf-value">${c.type}</div></div>
        <div class="cf-row"><div class="cf-label-left">Фаза:</div><div class="cf-value">${c.phase}</div></div>
        <div class="cf-row"><div class="cf-label-left">Длительность:</div><div class="cf-value">${duration}</div></div>
        <div class="cf-row"><div class="cf-label-left">Начало:</div><div class="cf-value">${day}.${month}.${year} ${hours}:${minutes}</div></div>
      </div>
    `;
  } catch (e) {
    errorEl.textContent = "Ошибка при запросе к API";
  }
});
