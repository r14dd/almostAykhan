let statsChart = null;

/**
 * Input: ()
 * Output: fetches stats, updates total count, and redraws chart
 */
async function loadStats() {
  try {
    const response = await fetch("/stats");
    const data = await response.json();
    const { per_day } = data;

    document.getElementById("totalCount").textContent = data.total || 0;

    const labels = per_day.map(d => d.day);
    const values = per_day.map(d => d.count);

    const ctx = document.getElementById("statsChart").getContext("2d");
    
    if (statsChart) {
      statsChart.destroy();
    }
    statsChart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "Gündəlik sorğular",
          data: values,
          borderColor: "#3de1ff",
          tension: 0.3,
          fill: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: "#ffffff"
            }
          }
        },
        scales: {
          x: {
            ticks: {
              color: "#ffffff"
            },
            grid: {
              color: "rgba(255, 255, 255, 0.1)"
            },
            border: {
              color: "rgba(255, 255, 255, 0.1)"
            }
          },
          y: {
            ticks: {
              color: "#ffffff"
            },
            grid: {
              color: "rgba(255, 255, 255, 0.1)"
            },
            border: {
              color: "rgba(255, 255, 255, 0.1)"
            }
          }
        }
      }
    });
  } catch (err) {
    console.error("Failed to load stats:", err);
  }
}

/**
 * Input: ()
 * Output: clears question input, answer text, and status text
 */
function clearUI() {
  document.getElementById("questionInput").value = "";
   document.getElementById("answer").textContent = "Sualınızı daxil edin.";
  document.getElementById("status").textContent = "";
}
document.getElementById("clearBtn").addEventListener("click", clearUI);


/**
 * Input: ()
 * Output: sends question to backend, renders answer/status, refreshes stats
 */
async function askQuestion() {
  const input = document.getElementById("questionInput");
  const answerEl = document.getElementById("answer");
  const btn = document.getElementById("askBtn");
  const status = document.getElementById("status");

  const query = input.value.trim();


  if (!query) {
    status.textContent = "Zəhmət olmasa sual daxil edin.";
    return;
  }

  btn.disabled = true;
  status.textContent = "Düşünürəm...";

  answerEl.textContent = "Düşünürəm...";

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: query }),
    });

    const data = await res.json();
    answerEl.textContent = data.answer || "Cavab tapılmadı.";
    status.textContent = "";
    loadStats();
  } catch (err) {
    answerEl.textContent = "Xəta baş verdi.";
    status.textContent = "Server xətası.";
  } finally {
    btn.disabled = false;
  }
}


document.getElementById("askBtn").addEventListener("click", askQuestion);

document.getElementById("questionInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") askQuestion();
});

loadStats();

/**
 * Input: uploaded JSON File object
 * Output: validates/parses JSON, sends it to /ingest, stores raw data in localStorage, and returns status message
 */
async function processIngestion(_file) {
  try {
    const text = await _file.text();
    const data = JSON.parse(text);

    localStorage.setItem("abb_chunks", text);

    const response = await fetch("/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chunks: data }),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "Server məlumatı qəbul etmədi.");
    }

    return `Uğurla tamamlandı: ${result.chunks} hissə yükləndi (${result.embedded} hissə vektorlaşdırıldı).`;

  } catch (err) {
    console.error("Ingestion error:", err);
    return err.name === "SyntaxError" ? "JSON faylı yanlışdır." : err.message;
  }
}

/**
 * Input: ()
 * Output: attaches upload change listener, triggers ingestion flow, updates upload status
 */
function setupUpload() {
  const fileInput = document.getElementById("dataFile");
  const status = document.getElementById("uploadStatus");

  if (!fileInput) return;

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    status.textContent = "İndekslənir... bu, 1-2 dəqiqə çəkə bilər";
    
    const message = await processIngestion(file);
    
    status.textContent = message;
    loadStats();
  });
}

setupUpload();
