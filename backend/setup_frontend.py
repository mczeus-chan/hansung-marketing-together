# -*- coding: utf-8 -*-
"""
frontend 파일 자동 생성 스크립트
backend 폴더에서 실행: python setup_frontend.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(BASE, "..", "frontend")
os.makedirs(FRONTEND, exist_ok=True)

def write(filename, content):
    path = os.path.join(FRONTEND, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] frontend/" + filename)

# ── index.html ─────────────────────────────────────
write("index.html", """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>한성 마케팅투게더</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

  <header>
    <div class="logo">HM</div>
    <div class="header-text">
      <h1>한성 마케팅투게더</h1>
      <p>Hansung University AI Marketing Agent</p>
    </div>
  </header>

  <div class="tab-bar">
    <button class="tab active" onclick="switchTab('press', this)">📰 보도자료 생성</button>
    <button class="tab" onclick="switchTab('short', this)">🎬 SNS 숏폼 제작</button>
    <button class="tab" onclick="switchTab('card', this)">🃏 카드뉴스 제작</button>
  </div>

  <!-- 보도자료 패널 -->
  <div class="panel active" id="panel-press">
    <div class="panel-title">📰 보도자료 생성</div>
    <p class="panel-desc">부서 정보와 핵심 내용을 입력하면 AI가 보도자료 초안을 작성합니다.</p>
    <label>부서명</label>
    <input type="text" id="dept-name" placeholder="예: 교무처, 학생처" />
    <label>행사·사업 유형</label>
    <select id="press-type">
      <option value="">선택하세요</option>
      <option>학사 행사</option>
      <option>연구 성과</option>
      <option>산학협력</option>
      <option>학생 활동</option>
      <option>취업·창업</option>
      <option>기타</option>
    </select>
    <label>핵심 내용 요약</label>
    <textarea id="press-summary" rows="5" placeholder="행사의 목적, 일시, 장소, 주요 내용을 간략히 입력하세요."></textarea>
    <button class="btn-primary" onclick="generatePress()">✨ AI 보도자료 생성</button>
    <div class="result-box" id="press-result" style="display:none;">
      <div class="result-label">생성 결과</div>
      <pre id="press-output"></pre>
    </div>
  </div>

  <!-- 숏폼 패널 -->
  <div class="panel" id="panel-short">
    <div class="panel-title">🎬 SNS 숏폼 제작</div>

    <!-- 진행 단계 -->
    <div class="progress-steps">
      <div class="progress-step active" id="step-1">
        <div class="step-circle">1</div>
        <div class="step-label">콘티 생성</div>
      </div>
      <div class="step-line"></div>
      <div class="progress-step" id="step-2">
        <div class="step-circle">2</div>
        <div class="step-label">이미지 생성</div>
      </div>
      <div class="step-line"></div>
      <div class="progress-step" id="step-3">
        <div class="step-circle">3</div>
        <div class="step-label">이미지 업로드</div>
      </div>
      <div class="step-line"></div>
      <div class="progress-step" id="step-4">
        <div class="step-circle">4</div>
        <div class="step-label">영상 제작</div>
      </div>
    </div>

    <!-- STEP 1: 콘티 생성 -->
    <div class="step-panel" id="step-panel-1">
      <p class="panel-desc">주제와 각 콘티 컨셉을 입력하면 AI가 이미지 프롬프트를 생성합니다.</p>
      <label>영상 주제</label>
      <input type="text" id="short-topic" placeholder="예: 2025 한성대학교 봄 축제" />
      <label>영상 분위기</label>
      <select id="short-mood">
        <option>역동적·에너지</option>
        <option>감성·따뜻함</option>
        <option>정보·깔끔함</option>
        <option>트렌디·힙</option>
      </select>
      <div class="conti-input-section">
        <div class="conti-input-header">5개 콘티 컨셉 입력 <span class="conti-hint">비워두면 AI가 자동 구성합니다</span></div>
        <div class="conti-input-row"><span class="conti-badge">콘티 1</span><input type="text" id="conti-1" placeholder="예: 상상부기가 벚꽃 캠퍼스를 걷는 장면" /></div>
        <div class="conti-input-row"><span class="conti-badge">콘티 2</span><input type="text" id="conti-2" placeholder="예: 친구들과 축제 부스에서 노는 장면" /></div>
        <div class="conti-input-row"><span class="conti-badge">콘티 3</span><input type="text" id="conti-3" placeholder="예: 무대에서 춤추는 장면" /></div>
        <div class="conti-input-row"><span class="conti-badge">콘티 4</span><input type="text" id="conti-4" placeholder="예: 친구들과 음식을 나눠먹는 장면" /></div>
        <div class="conti-input-row"><span class="conti-badge">콘티 5</span><input type="text" id="conti-5" placeholder="예: 모두 모여 기념사진 찍는 마무리 장면" /></div>
      </div>
      <button class="btn-primary" onclick="generateShortform()">✨ 이미지 프롬프트 생성</button>
      <div id="short-loading" style="display:none; text-align:center; padding:32px; color:#888; font-size:14px; line-height:2.2;">
        ⏳ AI가 콘티별 이미지 프롬프트를 생성 중입니다...
      </div>
      <div id="short-prompt-grid" style="margin-top:16px;"></div>
    </div>

    <!-- STEP 2: 이미지 생성 안내 -->
    <div class="step-panel" id="step-panel-2" style="display:none;">
      <div class="guide-box">
        <div class="guide-title">📸 ChatGPT로 이미지 10장 생성하기</div>
        <div class="guide-steps">
          <div class="guide-item">
            <span class="guide-num">1</span>
            <span>아래 프롬프트를 복사해서 <strong>ChatGPT → DALL-E</strong>에 붙여넣기</span>
          </div>
          <div class="guide-item">
            <span class="guide-num">2</span>
            <span>각 콘티별 <strong>시작 이미지 + 종료 이미지</strong> 총 10장 생성</span>
          </div>
          <div class="guide-item">
            <span class="guide-num">3</span>
            <span>생성된 이미지를 저장 후 아래 버튼 클릭</span>
          </div>
        </div>
      </div>
      <div id="guide-prompt-grid"></div>
      <button class="btn-primary" onclick="goToStep(3)" style="margin-top:16px;">✅ 이미지 준비 완료 → 업로드하기</button>
    </div>

    <!-- STEP 3: 이미지 업로드 -->
    <div class="step-panel" id="step-panel-3" style="display:none;">
      <p class="panel-desc">ChatGPT로 생성한 이미지를 콘티별로 업로드해주세요.</p>
      <div id="video-upload-grid"></div>
      <button class="btn-primary" onclick="goToStep(4)" style="margin-top:16px;">🎬 영상 제작 단계로 이동</button>
    </div>

    <!-- STEP 4: 영상 제작 -->
    <div class="step-panel" id="step-panel-4" style="display:none;">
      <p class="panel-desc">Kling AI가 이미지를 영상으로 변환하고 하나로 합칩니다.</p>
      <button class="btn-primary" onclick="generateVideos()" id="video-start-btn">🎬 영상 생성 시작</button>
      <div id="video-loading" style="display:none; text-align:center; padding:24px; color:#888; font-size:14px; line-height:2.2;">
        ⏳ Kling AI가 영상을 생성 중입니다...<br>
        <small>콘티당 약 1~2분 소요, 전체 5~10분 예상</small>
      </div>
      <div id="video-result-grid" style="margin-top:16px;"></div>
    </div>

  </div>

  <!-- 카드뉴스 패널 -->
  <div class="panel" id="panel-card">
    <div class="panel-title">🃏 카드뉴스 제작</div>
    <p class="panel-desc">행사 정보를 입력하면 4슬라이드 카드뉴스 텍스트를 자동 생성합니다.</p>
    <label>행사명</label>
    <input type="text" id="event-name" placeholder="예: 2025 학술제" />
    <label>주관 부서·단체</label>
    <input type="text" id="event-org" placeholder="예: 학생처" />
    <label>행사 일시</label>
    <input type="text" id="event-date" placeholder="예: 2025.05.20 (화) 14:00" />
    <label>행사 장소</label>
    <input type="text" id="event-place" placeholder="예: 우촌관 301호" />
    <label>참석자</label>
    <textarea id="event-attendees" rows="2" placeholder="예: 총장, 각 학과장, 학생 대표 외 ..."></textarea>
    <label>주요 내용</label>
    <textarea id="event-content" rows="5" placeholder="행사의 주요 내용, 성과, 특이사항을 입력하세요."></textarea>
    <button class="btn-primary" onclick="generateCardnews()">✨ AI 카드뉴스 생성</button>
    <div class="result-box" id="card-result" style="display:none;">
      <div class="result-label">생성 결과</div>
      <pre id="card-output"></pre>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
""")

print("")
print("=== 완료! ===")
print("Ctrl+Shift+R 로 브라우저 새로고침하세요.")
