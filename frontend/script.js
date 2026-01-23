const API_BASE = "http://127.0.0.1:8000";

// Карта фаз на русский
const phaseMap = {
  "FINISHED": "Завершенный",
  "BEFORE": "Будущий",
  "CODING": "Идет сейчас"
};

document.getElementById("load-btn").addEventListener("click", async () => {
  const phase = document.getElementById("phase").value;
  const type = document.getElementById("type").value;
  const minD = document.getElementById("min-duration").value;
  const maxD = document.getElementById("max-duration").value;

  const errorEl = document.getElementById("cf-error");
  const resultEl = document.getElementById("cf-result");
  const statsEl = document.getElementById("stats");

  errorEl.textContent = "";
  resultEl.innerHTML = "";
  statsEl.innerHTML = "";

  const params = new URLSearchParams();
  if (phase) params.append("phase", phase);
  if (type) params.append("contest_type", type);
  if (minD) params.append("min_duration", minD);
  if (maxD) params.append("max_duration", maxD);

  try {
    const res = await fetch(`${API_BASE}/codeforces/contests?${params}`);
    const data = await res.json();

    // --- статистика ---
    statsEl.innerHTML = `
      <b>Найдено контестов:</b> ${data.stats.total}<br>
      <b>Средняя длительность:</b> ${data.stats.avg_duration} мин
    `;

    if (data.contests.length === 0) {
      resultEl.innerHTML =
        "<div class='meta'>Контесты не найдены по заданным фильтрам</div>";
      return;
    }

    // --- топ 3 с русскими фазами и датой ---
    resultEl.innerHTML = `
      <div class="top-title">
        🏆 <b>Топ-3 последних контеста</b>
      </div>
    ` + data.contests.map((c, idx) => {
      const date = new Date(c.startTime);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const dateStr = `${day}.${month}.${year}`;

      return `
        <div class="contest">
          <div class="name">${idx + 1}️⃣ ${c.name}</div>
          <div class="meta">
            ${c.type} • ${phaseMap[c.phase] || c.phase} • ${dateStr} • ${c.durationMinutes} мин
          </div>
        </div>
      `;
    }).join("");

  } catch (e) {
    errorEl.textContent = "Ошибка при загрузке данных";
    console.error(e);
  }
});
