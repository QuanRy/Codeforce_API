const API_BASE = "http://127.0.0.1:8000";

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

    statsEl.innerHTML = `
      <b>Найдено контестов:</b> ${data.stats.total}<br>
      <b>Средняя длительность:</b> ${data.stats.avg_duration} мин
    `;

    resultEl.innerHTML = data.contests.map(c => `
      <div class="contest">
        <div class="name">${c.name}</div>
        <div class="meta">
          ${c.type} • ${c.phase} • ${c.durationMinutes} мин
        </div>
      </div>
    `).join("");

  } catch (e) {
    errorEl.textContent = "Ошибка при загрузке данных";
  }
});
