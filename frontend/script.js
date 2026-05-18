const API_BASE = "http://localhost:5000/api";

// 탭 전환
function switchTab(name, el) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  el.classList.add("active");
  document.getElementById("panel-" + name).classList.add("active");
}

// 로딩 상태 표시
function setLoading(btnEl, resultId, outputId, isLoading) {
  btnEl.disabled = isLoading;
  btnEl.textContent = isLoading ? "⏳ 생성 중..." : btnEl.dataset.label;
  if (isLoading) {
    document.getElementById(resultId).style.display = "block";
    document.getElementById(outputId).textContent = "AI가 생성 중입니다. 잠시만 기다려주세요...";
  }
}

// ── 보도자료 생성 ──────────────────────────────────
async function generatePress() {
  const btn = document.querySelector("#panel-press .btn-primary");
  btn.dataset.label = btn.textContent;

  const body = {
    dept_name:  document.getElementById("dept-name").value,
    press_type: document.getElementById("press-type").value,
    summary:    document.getElementById("press-summary").value,
  };

  if (!body.summary) { alert("핵심 내용 요약을 입력해주세요."); return; }

  setLoading(btn, "press-result", "press-output", true);
  try {
    const res  = await fetch(`${API_BASE}/press`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    document.getElementById("press-output").textContent = data.result;
    btn.textContent = "✨ AI 보도자료 생성";
    btn.disabled = false;
  } catch (e) {
    document.getElementById("press-output").textContent = "오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.";
    btn.textContent = "✨ AI 보도자료 생성";
    btn.disabled = false;
  }
}

// ── 숏폼 콘티 생성 ────────────────────────────────
async function generateShortform() {
  const btn = document.querySelector("#panel-short .btn-primary");
  btn.dataset.label = btn.textContent;

  const body = {
    topic:  document.getElementById("short-topic").value,
    mood:   document.getElementById("short-mood").value,
    engine: document.getElementById("short-engine").value,
  };

  if (!body.topic) { alert("영상 주제를 입력해주세요."); return; }

  setLoading(btn, "short-result", "short-output", true);
  try {
    const res  = await fetch(`${API_BASE}/shortform`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    document.getElementById("short-output").textContent = data.result;
    btn.textContent = "✨ 5개 콘티 AI 생성";
    btn.disabled = false;
  } catch (e) {
    document.getElementById("short-output").textContent = "오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.";
    btn.textContent = "✨ 5개 콘티 AI 생성";
    btn.disabled = false;
  }
}

// ── 카드뉴스 생성 ─────────────────────────────────
async function generateCardnews() {
  const btn = document.querySelector("#panel-card .btn-primary");
  btn.dataset.label = btn.textContent;

  const body = {
    event_name:      document.getElementById("event-name").value,
    event_org:       document.getElementById("event-org").value,
    event_date:      document.getElementById("event-date").value,
    event_place:     document.getElementById("event-place").value,
    event_attendees: document.getElementById("event-attendees").value,
    event_content:   document.getElementById("event-content").value,
  };

  if (!body.event_name) { alert("행사명을 입력해주세요."); return; }

  setLoading(btn, "card-result", "card-output", true);
  try {
    const res  = await fetch(`${API_BASE}/cardnews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    document.getElementById("card-output").textContent = data.result;
    btn.textContent = "✨ AI 카드뉴스 생성";
    btn.disabled = false;
  } catch (e) {
    document.getElementById("card-output").textContent = "오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.";
    btn.textContent = "✨ AI 카드뉴스 생성";
    btn.disabled = false;
  }
}
