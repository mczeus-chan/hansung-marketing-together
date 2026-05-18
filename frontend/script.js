const API_BASE = "http://localhost:5000/api";

// 탭 전환
function switchTab(name, el) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  el.classList.add("active");
  document.getElementById("panel-" + name).classList.add("active");
}

// 로딩 상태
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

// ── 숏폼 콘티 + 이미지 10장 생성 ─────────────────
async function generateShortform() {
  const btn   = document.querySelector("#panel-short .btn-primary");
  const topic = document.getElementById("short-topic").value;
  const mood  = document.getElementById("short-mood").value;

  if (!topic) { alert("영상 주제를 입력해주세요."); return; }

  btn.disabled = true;
  btn.textContent = "⏳ 생성 중...";

  var loading = document.getElementById("short-loading");
  var result  = document.getElementById("short-result");
  var grid    = document.getElementById("short-image-grid");

  if (loading) loading.style.display = "block";
  if (result)  result.style.display  = "none";
  if (grid)    grid.innerHTML = "";

  try {
    const res  = await fetch(`${API_BASE}/shortform`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: topic, mood: mood }),
    });
    const data = await res.json();

    if (data.error) {
      if (loading) loading.style.display = "none";
      alert("오류: " + data.error);
      btn.disabled = false;
      btn.textContent = "✨ 콘티 생성 + 이미지 10장 제작";
      return;
    }

    renderImageGrid(data.contis, data.images);

    if (loading) loading.style.display = "none";
    if (result)  result.style.display  = "block";

  } catch (e) {
    if (loading) loading.style.display = "none";
    alert("오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.");
  }

  btn.disabled = false;
  btn.textContent = "✨ 콘티 생성 + 이미지 10장 제작";
}

// 프렌즈 이름 한국어 변환
var FRIENDS_KO = {
  "white chicken": "🐔 흰 닭",
  "brown chicken": "🐔 갈색 닭",
  "cat":           "🐱 고양이",
  "frog":          "🐸 개구리",
};

// 콘티별 이미지 그리드 렌더링
function renderImageGrid(contis, images) {
  var grid = document.getElementById("short-image-grid");
  grid.innerHTML = "";

  contis.forEach(function(conti) {
    var num      = conti.conti_number;
    var friends  = conti.friends || [];
    var startImg = null;
    var endImg   = null;

    images.forEach(function(img) {
      if (img.conti_number === num && img.image_type === "start") startImg = img;
      if (img.conti_number === num && img.image_type === "end")   endImg   = img;
    });

    var friendBadges = '<div class="friends-row"><span class="friend-badge main-badge">🐢 상상부기</span>';
    friends.forEach(function(f) {
      var ko = FRIENDS_KO[f.toLowerCase()] || f;
      friendBadges += '<span class="friend-badge sub-badge">' + ko + '</span>';
    });
    friendBadges += '</div>';

    var startHtml = startImg && startImg.url
      ? '<img src="' + startImg.url + '" alt="콘티' + num + ' 시작" />'
      : '<div class="image-error">⚠️ 이미지 생성 실패</div>';

    var endHtml = endImg && endImg.url
      ? '<img src="' + endImg.url + '" alt="콘티' + num + ' 종료" />'
      : '<div class="image-error">⚠️ 이미지 생성 실패</div>';

    var block = document.createElement("div");
    block.className = "conti-block";
    block.innerHTML =
      '<div class="conti-header">' +
        '<span class="conti-num">콘티 ' + num + '</span>' +
        '<span class="conti-title">' + conti.title + '</span>' +
      '</div>' +
      '<p class="conti-desc">' + conti.description + '</p>' +
      friendBadges +
      '<div class="image-pair">' +
        '<div class="image-item">' +
          '<div class="image-label start-label">▶ 시작 이미지</div>' +
          startHtml +
        '</div>' +
        '<div class="image-item">' +
          '<div class="image-label end-label">⏹ 종료 이미지</div>' +
          endHtml +
        '</div>' +
      '</div>';

    grid.appendChild(block);
  });
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
