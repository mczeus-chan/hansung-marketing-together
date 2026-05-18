# 🎯 한성 마케팅투게더 (Hansung Marketing Together)

> 한성대학교 AI 마케팅 에이전트 — 보도자료 자동 생성 · SNS 숏폼 콘티 제작 · 교내 카드뉴스 생성

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?style=flat-square&logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 프로젝트 소개

한성대학교 각 부서 및 구성원이 행사·사업 자료를 업로드하면,
AI가 자동으로 **보도자료**, **SNS 숏폼 영상 콘티**, **교내 카드뉴스**를 생성해주는 마케팅 지원 에이전트입니다.

| 기능 | 설명 |
|------|------|
| 📰 보도자료 생성 | 계획안 업로드 → GPT 기반 역삼각형 구조 기사 자동 작성 |
| 🎬 SNS 숏폼 제작 | 주제 입력 → 5개 콘티 프롬프트 자동 생성 (Grok/Kling 연동) |
| 🃏 카드뉴스 제작 | 행사 정보 입력 → 4슬라이드 카드뉴스 텍스트 자동 생성 |

---

## 🎥 데모 영상

> 영상 링크를 여기에 추가하세요
> 예: https://youtu.be/xxxxxxxx

---

## 📁 폴더 구조

```
hansung-marketing-together/
│
├── backend/                  # Python 백엔드 (Flask)
│   ├── app.py                # 서버 진입점
│   ├── routes/
│   │   ├── press.py          # 보도자료 생성 API
│   │   ├── shortform.py      # 숏폼 콘티 생성 API
│   │   └── cardnews.py       # 카드뉴스 생성 API
│   ├── prompts/
│   │   ├── press_prompt.txt      # 보도자료용 GPT 프롬프트
│   │   ├── shortform_prompt.txt  # 숏폼 콘티용 GPT 프롬프트
│   │   └── cardnews_prompt.txt   # 카드뉴스용 GPT 프롬프트
│   └── requirements.txt      # Python 패키지 목록
│
├── frontend/                 # HTML/CSS/JS 프론트엔드
│   ├── index.html            # 메인 페이지 (탭 구조)
│   ├── style.css             # 스타일시트
│   └── script.js             # API 호출 및 결과 렌더링
│
├── .env.example              # 환경변수 예시 (API 키 설정)
├── .gitignore                # Git 제외 파일 목록
└── README.md                 # 이 파일
```

---

## ⚙️ 설치 및 실행 방법

### 1단계 — 코드 내려받기

```bash
git clone https://github.com/본인아이디/hansung-marketing-together.git
cd hansung-marketing-together
```

### 2단계 — OpenAI API 키 설정

`.env.example` 파일을 복사해서 `.env` 파일을 만드세요.

```bash
cp .env.example .env
```

`.env` 파일을 열어서 아래 내용을 입력하세요.

```
OPENAI_API_KEY=여기에_본인의_API_키_입력
```

> OpenAI API 키는 https://platform.openai.com/api-keys 에서 발급받을 수 있어요.

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

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 (필수) | `sk-...` |

---

## 🛠 사용 기술

- **백엔드**: Python 3.10+, Flask, OpenAI API (GPT-4o)
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript
- **AI 연동**: OpenAI GPT-4o (보도자료·카드뉴스), Grok / Kling AI (숏폼 영상, 추후 연동)

---

## 📋 기능 상세

### 1) 보도자료 생성
- 부서 계획안 파일(TXT/PDF) 업로드
- 역삼각형 구조(핵심 → 배경 → 상세)로 기사 자동 작성
- 한성대 보도자료 작성 노하우 반영 (추후 업데이트 예정)

### 2) SNS 숏폼 제작
- 1개 주제 입력 → 5개 콘티 자동 생성
- 각 콘티별 시작 이미지·종료 이미지 프롬프트 (영어) 제공
- Grok 또는 Kling AI에 프롬프트 그대로 입력하면 영상 생성 가능

### 3) 카드뉴스 제작
- 행사명·일시·장소·참석자·주요내용 입력
- 4슬라이드 구성 자동 생성
  - Slide 0: 제목 (캐치프레이즈 포함)
  - Slide 1: 개요 (사진 캡션 포함)
  - Slide 2: 참석자 소개 (사진 캡션 포함)
  - Slide 3: 행사 주요내용 (사진 캡션 포함)

---

## 📎 제출 링크

| 구분 | 링크 |
|------|------|
| 🎥 데모 영상 | [바로가기](여기에_영상_링크) |
| 📄 결과 보고서 | [바로가기](여기에_보고서_링크) |
| 💻 소스 코드 | [바로가기](여기에_GitHub_링크) |

---

## 👥 팀 정보

| 이름 | 역할 |
|------|------|
| 홍길동 | 기획 · 개발 · 디자인 |

> 한성대학교 × 2025 공모전 출품작

---

## 📄 라이선스

MIT License © 2025 Hansung Marketing Together
