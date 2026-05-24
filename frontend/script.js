const API_BASE = "http://localhost:5000/api";

// 전역 변수
var _lastContis = [];
var _uploadedImages = {};

// ── 탭 전환 ───────────────────────────────────────
function switchTab(name, el) {
  document.querySelectorAll(".tab").forEach(function(t) { t.classList.remove("active"); });
  document.querySelectorAll(".panel").forEach(function(p) { p.classList.remove("active"); });
  el.classList.add("active");
  document.getElementById("panel-" + name).classList.add("active");
}

// ── 단계 전환 ─────────────────────────────────────
function goToStep(num) {
  for (var i = 1; i <= 4; i++) {
    var panel = document.getElementById("step-panel-" + i);
    var step  = document.getElementById("step-" + i);
    if (panel) panel.style.display = "none";
    if (step) {
      step.classList.remove("active", "done");
      if (i < num) step.classList.add("done");
    }
  }
  // 라인 업데이트
  document.querySelectorAll(".step-line").forEach(function(line, idx) {
    if (idx < num - 1) line.classList.add("done");
    else line.classList.remove("done");
  });

  var currentPanel = document.getElementById("step-panel-" + num);
  var currentStep  = document.getElementById("step-" + num);
  if (currentPanel) currentPanel.style.display = "block";
  if (currentStep)  currentStep.classList.add("active");

  // step3 진입 시 업로드 UI 표시
  if (num === 3 && _lastContis.length > 0) {
    buildUploadGrid(_lastContis);
  }

  window.scrollTo({top: 0, behavior: "smooth"});
}

// ── 클립보드 복사 ──────────────────────────────────
function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(function() {
    var orig = btn.textContent;
    btn.textContent = "✅ 복사됨!";
    setTimeout(function() { btn.textContent = orig; }, 1500);
  });
}

// ── PDF 업로드 처리 ───────────────────────────────
var _pdfFile = null;

function handlePdfUpload(input) {
  if (!input.files || !input.files[0]) return;
  _pdfFile = input.files[0];

  var preview = document.getElementById("pdf-preview");
  preview.innerHTML =
    '<div class="pdf-file-info">' +
      '<span class="pdf-file-icon">📄</span>' +
      '<span class="pdf-file-name">' + _pdfFile.name + '</span>' +
      '<span class="pdf-file-size">(' + (Math.round(_pdfFile.size / 1024)) + 'KB)</span>' +
      '<button onclick="clearPdf()" class="pdf-clear-btn">✕</button>' +
    '</div>';
  preview.style.display = "block";
  document.getElementById("pdf-upload-box").style.borderColor = "var(--hsu-red, #C8001E)";
}

function clearPdf() {
  _pdfFile = null;
  document.getElementById("pdf-input").value = "";
  document.getElementById("pdf-preview").style.display = "none";
  document.getElementById("pdf-upload-box").style.borderColor = "";
}

// ── 보도자료 생성 ──────────────────────────────────
async function generatePress() {
  var btn     = document.querySelector("#panel-press .btn-primary");
  var summary = document.getElementById("press-summary").value;

  if (!_pdfFile && !summary) {
    alert("PDF 파일을 업로드하거나 핵심 내용을 입력해주세요.");
    return;
  }

  btn.disabled = true;
  btn.textContent = "⏳ 생성 중...";
  document.getElementById("press-loading").style.display = "block";
  document.getElementById("press-result").style.display  = "none";

  try {
    var res;

    if (_pdfFile) {
      // PDF 방식
      var formData = new FormData();
      formData.append("pdf",        _pdfFile);
      formData.append("dept_name",  document.getElementById("dept-name").value);
      formData.append("press_type", document.getElementById("press-type").value);
      formData.append("summary",    summary);
      res = await fetch(API_BASE + "/press", { method: "POST", body: formData });
    } else {
      // 일반 텍스트 방식
      res = await fetch(API_BASE + "/press", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dept_name:  document.getElementById("dept-name").value,
          press_type: document.getElementById("press-type").value,
          summary:    summary,
        }),
      });
    }

    var data = await res.json();
    document.getElementById("press-loading").style.display = "none";
    document.getElementById("press-result").style.display  = "block";
    document.getElementById("press-output").textContent    = data.result || data.error;

    // 다운로드 버튼 표시
    if (data.result) {
      var dlBtn = document.getElementById("press-download-btn");
      if (dlBtn) dlBtn.style.display = "block";
    }

  } catch(e) {
    document.getElementById("press-loading").style.display = "none";
    document.getElementById("press-result").style.display  = "block";
    document.getElementById("press-output").textContent    = "오류가 발생했습니다.";
  }

  btn.disabled = false;
  btn.textContent = "✨ AI 보도자료 생성";
}

// ── 보도자료 Word 다운로드 ───────────────────────────
async function downloadPress() {
  var text = document.getElementById("press-output").textContent;
  if (!text) { alert("먼저 보도자료를 생성해주세요."); return; }

  var btn = document.getElementById("press-download-btn");
  btn.textContent = "⏳ 변환 중...";
  btn.disabled = true;

  try {
    var res = await fetch(API_BASE + "/press/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });

    var blob = await res.blob();
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement("a");
    a.href     = url;
    a.download = "한성대학교_보도자료.docx";
    a.click();
    URL.revokeObjectURL(url);

  } catch(e) {
    alert("다운로드 오류가 발생했습니다.");
  }

  btn.textContent = "⬇️ Word 파일 다운로드 (.docx)";
  btn.disabled = false;
}

// ── 숏폼 STEP 1: 콘티 + 프롬프트 생성 ────────────
async function generateShortform() {
  var btn   = document.querySelector("#step-panel-1 .btn-primary");
  var topic = document.getElementById("short-topic").value;
  var mood  = document.getElementById("short-mood").value;
  if (!topic) { alert("영상 주제를 입력해주세요."); return; }

  btn.disabled = true;
  btn.textContent = "⏳ 생성 중...";
  document.getElementById("short-loading").style.display = "block";
  document.getElementById("short-prompt-grid").innerHTML = "";

  var contis = [];
  for (var i = 1; i <= 5; i++) {
    contis.push({ concept: document.getElementById("conti-" + i).value });
  }

  try {
    var res  = await fetch(API_BASE + "/shortform", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: topic, mood: mood, contis: contis }),
    });
    var data = await res.json();

    if (data.error) {
      alert("오류: " + data.error);
      btn.disabled = false;
      btn.textContent = "✨ 이미지 프롬프트 생성";
      document.getElementById("short-loading").style.display = "none";
      return;
    }

    _lastContis = data.contis;
    document.getElementById("short-loading").style.display = "none";

    // step1에 프롬프트 표시
    renderPromptGrid(data.contis);

    // step2 가이드에도 프롬프트 표시
    renderGuidePromptGrid(data.contis);

    // step2로 이동
    goToStep(2);

  } catch(e) {
    alert("오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.");
    document.getElementById("short-loading").style.display = "none";
  }

  btn.disabled = false;
  btn.textContent = "✨ 이미지 프롬프트 생성";
}

// ── 프롬프트 그리드 렌더링 (step1용) ──────────────
var FRIENDS_KO = {
  "white chicken": "🐔 흰 닭",
  "brown chicken": "🐔 갈색 닭",
  "cat":           "🐱 고양이",
  "frog":          "🐸 개구리",
};

function renderPromptGrid(contis) {
  var grid = document.getElementById("short-prompt-grid");
  grid.innerHTML = "";

  // 다운로드 버튼
  var dlBtn = document.createElement("button");
  dlBtn.className = "btn-download";
  dlBtn.textContent = "⬇️ 전체 콘티 TXT 다운로드";
  dlBtn.onclick = downloadAllContis;
  grid.appendChild(dlBtn);

  contis.forEach(function(conti) {
    var num = conti.conti_number;
    var block = document.createElement("div");
    block.className = "prompt-block";
    block.innerHTML =
      '<div class="conti-header">' +
        '<span class="conti-num">콘티 ' + num + '</span>' +
        '<span class="conti-title">' + (conti.title || "") + '</span>' +
      '</div>' +
      '<p class="conti-concept">' + (conti.concept || "") + '</p>' +
      '<div class="hooking-box">' +
        '<span class="hooking-label">💬 후킹 문구</span>' +
        '<span class="hooking-text" id="hook-' + num + '">' + (conti.hooking || "") + '</span>' +
        '<button class="copy-btn" onclick="copyText(document.getElementById(\'hook-' + num + '\').textContent, this)">📋 복사</button>' +
      '</div>' +
      '<div class="prompt-section">' +
        '<div class="prompt-label start-label">▶ 시작 이미지 프롬프트</div>' +
        '<div class="prompt-text" id="start-' + num + '">' + (conti.start_image_prompt || "") + '</div>' +
        '<button class="copy-btn" onclick="copyText(document.getElementById(\'start-' + num + '\').textContent, this)">📋 복사</button>' +
      '</div>' +
      '<div class="prompt-section">' +
        '<div class="prompt-label end-label">⏹ 종료 이미지 프롬프트</div>' +
        '<div class="prompt-text" id="end-' + num + '">' + (conti.end_image_prompt || "") + '</div>' +
        '<button class="copy-btn" onclick="copyText(document.getElementById(\'end-' + num + '\').textContent, this)">📋 복사</button>' +
      '</div>';
    grid.appendChild(block);
  });
}

// ── 가이드 프롬프트 그리드 (step2용) ──────────────
function renderGuidePromptGrid(contis) {
  var grid = document.getElementById("guide-prompt-grid");
  if (!grid) return;
  grid.innerHTML = "";

  contis.forEach(function(conti) {
    var num = conti.conti_number;
    var block = document.createElement("div");
    block.className = "prompt-block";
    block.innerHTML =
      '<div class="conti-header">' +
        '<span class="conti-num">콘티 ' + num + '</span>' +
        '<span class="conti-title">' + (conti.title || "") + '</span>' +
      '</div>' +
      '<div class="hooking-box">' +
        '<span class="hooking-label">💬 후킹</span>' +
        '<span class="hooking-text">' + (conti.hooking || "") + '</span>' +
      '</div>' +
      '<div class="prompt-section">' +
        '<div class="prompt-label start-label">▶ 시작 이미지 프롬프트</div>' +
        '<div class="prompt-text" id="gs-' + num + '">' + (conti.start_image_prompt || "") + '</div>' +
        '<button class="copy-btn" onclick="copyText(document.getElementById(\'gs-' + num + '\').textContent, this)">📋 복사</button>' +
      '</div>' +
      '<div class="prompt-section">' +
        '<div class="prompt-label end-label">⏹ 종료 이미지 프롬프트</div>' +
        '<div class="prompt-text" id="ge-' + num + '">' + (conti.end_image_prompt || "") + '</div>' +
        '<button class="copy-btn" onclick="copyText(document.getElementById(\'ge-' + num + '\').textContent, this)">📋 복사</button>' +
      '</div>';
    grid.appendChild(block);
  });
}

// ── 전체 다운로드 ──────────────────────────────────
function downloadAllContis() {
  var topic = document.getElementById("short-topic").value || "숏폼";
  var lines = [];
  lines.push("========================================");
  lines.push("한성 마케팅투게더 — SNS 숏폼 콘티 프롬프트");
  lines.push("주제: " + topic);
  lines.push("생성일: " + new Date().toLocaleString("ko-KR"));
  lines.push("========================================\n");
  lines.push("[ 사용 방법 ]");
  lines.push("1. 각 콘티의 후킹 문구 → 영상 자막으로 활용");
  lines.push("2. 시작/종료 이미지 프롬프트 → ChatGPT에 입력해 이미지 생성");
  lines.push("3. 생성된 이미지 → 에이전트에 업로드 후 Kling AI 영상 제작\n");
  lines.push("========================================\n");
  _lastContis.forEach(function(conti) {
    lines.push("[ 콘티 " + conti.conti_number + " ] " + (conti.title || ""));
    lines.push("컨셉: " + (conti.concept || ""));
    lines.push("💬 후킹 문구: " + (conti.hooking || ""));
    lines.push("");
    lines.push("▶ 시작 이미지 프롬프트:");
    lines.push(conti.start_image_prompt || "");
    lines.push("");
    lines.push("⏹ 종료 이미지 프롬프트:");
    lines.push(conti.end_image_prompt || "");
    lines.push("\n----------------------------------------\n");
  });
  var blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement("a");
  a.href     = url;
  a.download = topic + "_숏폼콘티프롬프트.txt";
  a.click();
  URL.revokeObjectURL(url);
}

// ── STEP 3: 이미지 업로드 UI ──────────────────────
function buildUploadGrid(contis) {
  var grid = document.getElementById("video-upload-grid");
  if (!grid) return;
  grid.innerHTML = "";
  _uploadedImages = {};

  contis.forEach(function(conti) {
    var num = conti.conti_number;
    var row = document.createElement("div");
    row.className = "video-upload-row";
    row.innerHTML =
      '<div class="video-upload-label">' +
        '<span class="conti-num">콘티 ' + num + '</span>' +
        '<span class="video-upload-title">' + (conti.title || "") + '</span>' +
      '</div>' +
      '<div class="video-upload-pair">' +
        '<div class="video-upload-item">' +
          '<div class="upload-item-label start-label">▶ 시작 이미지</div>' +
          '<input type="file" accept="image/*" id="upload-start-' + num + '" style="display:none;" onchange="previewImage(' + num + ', \'start\', this)" />' +
          '<label for="upload-start-' + num + '" class="upload-label-btn">📁 업로드</label>' +
          '<div id="preview-start-' + num + '" class="image-preview" style="display:none;"></div>' +
        '</div>' +
        '<div class="video-upload-item">' +
          '<div class="upload-item-label end-label">⏹ 종료 이미지</div>' +
          '<input type="file" accept="image/*" id="upload-end-' + num + '" style="display:none;" onchange="previewImage(' + num + ', \'end\', this)" />' +
          '<label for="upload-end-' + num + '" class="upload-label-btn">📁 업로드</label>' +
          '<div id="preview-end-' + num + '" class="image-preview" style="display:none;"></div>' +
        '</div>' +
      '</div>';
    grid.appendChild(row);
  });
}

function previewImage(num, type, input) {
  if (!input.files || !input.files[0]) return;
  if (!_uploadedImages[num]) _uploadedImages[num] = {};
  _uploadedImages[num][type] = input.files[0];
  var reader = new FileReader();
  reader.onload = function(e) {
    var preview = document.getElementById("preview-" + type + "-" + num);
    preview.innerHTML = '<img src="' + e.target.result + '" style="width:70px; height:110px; object-fit:cover; border-radius:6px;" /><span style="font-size:11px; color:#22c55e; margin-left:6px;">✅</span>';
    preview.style.display = "flex";
    preview.style.alignItems = "center";
  };
  reader.readAsDataURL(input.files[0]);
}

// ── 이미지 fal.ai 업로드 ──────────────────────────
async function uploadImageToFal(file) {
  var safeFile = new File([file], "upload.png", {type: "image/png"});
  var formData = new FormData();
  formData.append("file", safeFile);
  var res  = await fetch(API_BASE + "/upload-image", {
    method: "POST",
    body: formData
  });
  var text = await res.text();
  try {
    var data = JSON.parse(text);
    return data.url || null;
  } catch(e) {
    return null;
  }
}

// ── STEP 4: 영상 생성 ─────────────────────────────
async function generateVideos() {
  var btn = document.getElementById("video-start-btn");

  if (Object.keys(_uploadedImages).length === 0) {
    alert("step 3에서 이미지를 먼저 업로드해주세요!");
    return;
  }

  if (btn) { btn.disabled = true; btn.textContent = "⏳ 생성 중..."; }
  document.getElementById("video-loading").style.display = "block";
  document.getElementById("video-result-grid").innerHTML = "";
  document.getElementById("video-loading").innerHTML =
    "⏳ 이미지를 서버에 업로드 중입니다...";

  var contiData = [];
  for (var i = 0; i < _lastContis.length; i++) {
    var conti = _lastContis[i];
    var num   = conti.conti_number;
    if (!_uploadedImages[num]) continue;
    var sFile = _uploadedImages[num]["start"];
    var eFile = _uploadedImages[num]["end"];
    if (!sFile) continue;

    var sUrl = await uploadImageToFal(sFile);
    var eUrl = eFile ? await uploadImageToFal(eFile) : "";

    if (!sUrl) {
      alert("콘티 " + num + " 이미지 업로드 실패!");
      if (btn) { btn.disabled = false; btn.textContent = "🎬 영상 생성 시작"; }
      document.getElementById("video-loading").style.display = "none";
      return;
    }
    contiData.push({
      conti_number: num,
      start_url:    sUrl,
      end_url:      eUrl,
      prompt:       conti.start_image_prompt || "",
    });
  }

  if (contiData.length === 0) {
    alert("최소 1개 콘티의 이미지를 업로드해주세요!");
    if (btn) { btn.disabled = false; btn.textContent = "🎬 영상 생성 시작"; }
    document.getElementById("video-loading").style.display = "none";
    return;
  }

  document.getElementById("video-loading").innerHTML =
    "⏳ Kling AI가 영상을 생성 중입니다...<br><small>콘티당 약 1~2분, 전체 5~10분 예상</small>";

  try {
    var res = await fetch(API_BASE + "/video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contis: contiData, mood: document.getElementById("short-mood").value }),
    });

    var contentType = res.headers.get("Content-Type") || "";
    document.getElementById("video-loading").style.display = "none";

    if (contentType.includes("video")) {
      var blob = await res.blob();
      var url  = URL.createObjectURL(blob);
      var grid = document.getElementById("video-result-grid");
      grid.innerHTML =
        "<div class='video-result-title'>🎬 완성된 숏폼 영상</div>" +
        "<div class='video-result-block'>" +
          "<video controls style='width:100%; border-radius:8px; margin-top:8px;'>" +
            "<source src='" + url + "' type='video/mp4' />" +
          "</video>" +
          "<a href='" + url + "' download='hansung_shortform.mp4' class='copy-btn' style='display:inline-block; margin-top:12px; padding:10px 20px; background:#0D1B3E; color:white; border-radius:8px; text-decoration:none; font-weight:600;'>⬇️ 숏폼 영상 다운로드</a>" +
        "</div>";
    } else {
      var text = await res.text();
      try {
        var data = JSON.parse(text);
        alert("오류: " + (data.error || text));
      } catch(e) {
        alert("오류: " + text.substring(0, 200));
      }
    }
  } catch(e) {
    document.getElementById("video-loading").style.display = "none";
    alert("오류가 발생했습니다: " + e.message);
  }

  if (btn) { btn.disabled = false; btn.textContent = "🎬 영상 생성 시작"; }
}

// ── 카드뉴스 생성 ─────────────────────────────────
var _cardnewsHTML = "";

async function generateCardnews() {
  var btn = document.querySelector("#panel-card .btn-primary");
  var body = {
    event_name:      document.getElementById("event-name").value,
    event_org:       document.getElementById("event-org").value,
    event_date:      document.getElementById("event-date").value,
    event_place:     document.getElementById("event-place").value,
    event_attendees: document.getElementById("event-attendees").value,
    event_content:   document.getElementById("event-content").value,
  };
  if (!body.event_name) { alert("행사명을 입력해주세요."); return; }

  btn.disabled = true;
  btn.textContent = "⏳ 생성 중...";
  document.getElementById("card-loading").style.display = "block";
  document.getElementById("card-result").style.display  = "none";

  try {
    var res  = await fetch(API_BASE + "/cardnews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    var data = await res.json();

    if (data.error) {
      alert("오류: " + data.error);
      btn.disabled = false;
      btn.textContent = "✨ AI 카드뉴스 생성";
      document.getElementById("card-loading").style.display = "none";
      return;
    }

    _cardnewsHTML = data.html;
    document.getElementById("card-loading").style.display = "none";
    document.getElementById("card-result").style.display  = "block";
    document.getElementById("card-info").innerHTML =
      "✅ <strong>" + data.total + "슬라이드</strong> 카드뉴스가 생성됐어요! " +
      "아래 버튼을 눌러 확인하고 PDF로 저장하세요.";

    // 자동으로 새 탭 열기
    openCardnews();

  } catch(e) {
    alert("오류가 발생했습니다.");
    document.getElementById("card-loading").style.display = "none";
  }

  btn.disabled = false;
  btn.textContent = "✨ AI 카드뉴스 생성";
}

function openCardnews() {
  if (!_cardnewsHTML) { alert("먼저 카드뉴스를 생성해주세요."); return; }
  var blob = new Blob([_cardnewsHTML], {type: "text/html;charset=utf-8"});
  var url  = URL.createObjectURL(blob);
  window.open(url, "_blank");
}
