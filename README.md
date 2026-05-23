[README.md](https://github.com/user-attachments/files/28173460/README.md)
# 🎯 한성 마케팅투게더 (Hansung Marketing Together)

> 한성대학교 AI 마케팅 에이전트 — 보도자료 자동 생성 · SNS 숏폼 제작 · 교내 카드뉴스 생성

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?style=flat-square&logo=openai)
![Kling AI](https://img.shields.io/badge/Kling-AI_Video-purple?style=flat-square)
![fal.ai](https://img.shields.io/badge/fal.ai-Image_Upload-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 프로젝트 소개

한성대학교 각 부서 및 구성원이 행사·사업 자료를 입력하면,
AI가 자동으로 **보도자료**, **SNS 숏폼 영상**, **교내 카드뉴스**를 생성해주는 마케팅 지원 에이전트입니다.

| 기능 | 설명 |
|------|------|
| 📰 보도자료 생성 | 계획안 입력 → GPT-4o 기반 역삼각형 구조 기사 자동 작성 (한성대 노하우 반영) |
| 🎬 SNS 숏폼 제작 | 주제 + 콘티 입력 → 5개 콘티 프롬프트 생성 → Kling AI 영상 자동 합성 |
| 🃏 카드뉴스 제작 | 행사 정보 입력 → 한성대 스타일 HTML 카드뉴스 자동 생성 (랜덤 그라데이션) |

---

## 🎥 데모 영상

> 영상 링크를 여기에 추가하세요
> 예: https://youtu.be/xxxxxxxx

---

## 📁 폴더 구조

```
hansung-marketing-together/
│
├── backend/                        # Python 백엔드 (Flask)
│   ├── app.py                      # 서버 진입점
│   ├── requirements.txt            # Python 패키지 목록
│   ├── assets/                     # 캐릭터 이미지
│   │   ├── sangsang_bugi.png       # 상상부기 메인 캐릭터
│   │   └── sangsang_friends.png    # 상상부기 프렌즈
│   ├── routes/
│   │   ├── press.py                # 보도자료 생성 API
│   │   ├── shortform.py            # 숏폼 콘티 생성 API
│   │   ├── cardnews.py             # 카드뉴스 생성 API
│   │   └── video.py                # Kling AI 영상 생성 API
│   └── prompts/
│       ├── press_prompt.txt        # 보도자료 GPT 프롬프트
│       ├── shortform_prompt.txt    # 숏폼 콘티 GPT 프롬프트
│       └── cardnews_prompt.txt     # 카드뉴스 GPT 프롬프트
│
├── frontend/                       # HTML/CSS/JS 프론트엔드
│   ├── index.html                  # 메인 페이지
│   ├── style.css                   # 스타일시트
│   └── script.js                   # API 호출 및 UI 로직
│
├── .env.example                    # 환경변수 예시
├── .gitignore                      # Git 제외 파일 목록
└── README.md                       # 이 파일
```

---

## ⚙️ 설치 및 실행 방법

### 1단계 — 코드 내려받기

```bash
git clone https://github.com/본인아이디/hansung-marketing-together.git
cd hansung-marketing-together
```

### 2단계 — API 키 설정

`.env.example` 파일을 복사해서 `.env` 파일을 만드세요.

```bash
cp .env.example .env
```

`.env` 파일을 열어서 아래 내용을 입력하세요.

```
OPENAI_API_KEY=여기에_OpenAI_API_키_입력
FAL_KEY=여기에_fal.ai_API_키_입력
```

> - OpenAI API 키: https://platform.openai.com/api-keys
> - fal.ai API 키: https://fal.ai/dashboard/keys

### 3단계 — Python 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

### 4단계 — 서버 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 으로 접속하면 됩니다.

---

## 🔑 환경변수 목록

| 변수명 | 설명 | 발급처 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 키 (필수) | platform.openai.com |
| `FAL_KEY` | fal.ai API 키 (영상 생성 시 필요) | fal.ai |

---

## 🛠 사용 기술

- **백엔드**: Python 3.10+, Flask, OpenAI API (GPT-4o)
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript
- **AI 연동**:
  - OpenAI GPT-4o (보도자료·카드뉴스·숏폼 콘티)
  - fal.ai + Kling AI (이미지 업로드 및 영상 생성)
  - moviepy (영상 합치기)

---

## 📋 기능 상세

### 1) 보도자료 생성
- 부서명·행사 유형·핵심 내용 입력
- 역삼각형 구조(핵심 → 배경 → 상세)로 자동 작성
- 한성대 보도자료 노하우 반영
  - 첫 문장: `한성대학교(총장: 이창원)는` 으로 시작
  - 이후 본문: `한성대`로 축약
  - 고유명사 `〈 〉` 처리
  - 이창원 총장 코멘트 형식 자동 적용

### 2) SNS 숏폼 제작 (4단계)
- **① 콘티 생성**: 주제 + 5개 콘티 컨셉 입력 → AI가 프롬프트 + 후킹 문구 생성
- **② 이미지 생성**: 생성된 프롬프트를 ChatGPT DALL-E에 입력해 10장 이미지 제작
- **③ 이미지 업로드**: 콘티별 시작·종료 이미지 업로드
- **④ 영상 제작**: Kling AI가 5초 영상 5개 생성 → moviepy로 자동 합성

### 3) 카드뉴스 제작
- 행사 정보 입력 → GPT-4o가 슬라이드 콘텐츠 자동 생성
- 슬라이드 수 자동 조정 (기본 4장, 최대 6장)
- 한성대 스타일 HTML 카드뉴스 생성 (랜덤 그라데이션)
- 브라우저에서 바로 확인 + PDF 저장 가능
- 슬라이드 전체가 하나의 스토리 흐름으로 연결

---

## 👤 팀 정보

| 이름 | 역할 |
|------|------|
| 홍길동 | 기획 · 개발 · 디자인 |

> 한성대학교 × 2026 AX프론티어 공모전 출품작

---

## 📎 제출 링크

| 구분 | 링크 |
|------|------|
| 🎥 데모 영상 | [바로가기](여기에_영상_링크) |
| 📄 결과 보고서 | [바로가기](여기에_보고서_링크) |
| 💻 소스 코드 | [바로가기](여기에_GitHub_링크) |

---

## 📄 라이선스

MIT License © 2026 Hansung Marketing Together
