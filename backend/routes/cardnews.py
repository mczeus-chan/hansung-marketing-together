from flask import Blueprint, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os, json, re, random

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
cardnews_bp = Blueprint("cardnews", __name__)

def load_prompt():
    path = os.path.join(os.path.dirname(__file__), "../prompts/cardnews_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def respond(data, code=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        status=code,
        mimetype="application/json; charset=utf-8"
    )

# 안정적인 그라데이션 색상 팔레트
GRADIENT_PALETTES = [
    # 보라/주황 (레퍼런스1)
    ["#2D1B69", "#8B2FC9", "#E05D2B"],
    # 핑크/보라 (레퍼런스2)
    ["#C8A0D8", "#8B7BB8", "#4A4580"],
    # 청록/남색 (레퍼런스3)
    ["#7EC8C8", "#2B7BB8", "#1A3A6B"],
    # 딥블루/퍼플
    ["#1a1a5e", "#4a2c8a", "#8B4DB8"],
    # 네이비/청록
    ["#0D2137", "#1B5E8A", "#2BA8A8"],
    # 딥그린/티얼
    ["#1B4332", "#2D6A4F", "#52B788"],
    # 버건디/네이비
    ["#4A0E2D", "#8B1A4A", "#2D1B69"],
    # 인디고/바이올렛
    ["#1E1B4B", "#4338CA", "#7C3AED"],
    # 딥씨/코발트
    ["#0C2340", "#1A4B8C", "#2E86C1"],
    # 모브/로즈
    ["#4A1942", "#8B3A7E", "#C96B9E"],
]

GRADIENT_DIRECTIONS = [
    "135deg", "120deg", "150deg",
    "to bottom right", "to bottom",
    "160deg", "45deg", "to right"
]

def get_random_gradient():
    palette   = random.choice(GRADIENT_PALETTES)
    direction = random.choice(GRADIENT_DIRECTIONS)
    colors    = ", ".join(palette)
    return f"linear-gradient({direction}, {colors})"

def build_html(slides, event_name):
    gradient = get_random_gradient()

    slides_html = ""
    for i, slide in enumerate(slides):
        stype = slide.get("type", "content")
        label = slide.get("label", "")
        body  = slide.get("body", "")
        title = slide.get("title", "")
        subtitle = slide.get("subtitle", "")
        tags  = slide.get("tags", [])
        has_photo = "[PHOTO]" in tags
        has_logo  = "[LOGO]" in tags

        if stype == "title":
            slide_html = f'''
<div class="slide" style="background:{gradient};">
  <div class="slide-inner title-slide">
    <div class="title-text">
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
    </div>
    {"<div class='hsu-logo'>🏫 HSU 한성대학교</div>" if has_logo else ""}
  </div>
  <div class="slide-num">{i+1} / {len(slides)}</div>
</div>'''

        elif has_photo:
            slide_html = f'''
<div class="slide" style="background:{gradient};">
  <div class="slide-inner content-slide">
    {"<div class='label'>" + label + "</div>" if label else ""}
    <div class="photo-box">
      <div class="photo-placeholder">📷 사진 삽입</div>
    </div>
    <div class="body-text">{body}</div>
  </div>
  <div class="slide-num">{i+1} / {len(slides)}</div>
</div>'''

        else:
            slide_html = f'''
<div class="slide" style="background:{gradient};">
  <div class="slide-inner content-slide">
    {"<div class='label'>" + label + "</div>" if label else ""}
    <div class="body-text body-only">{body}</div>
  </div>
  <div class="slide-num">{i+1} / {len(slides)}</div>
</div>'''

        slides_html += slide_html

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{event_name} 카드뉴스</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
         background:#1a1a1a; padding:20px; }}
  h2 {{ color:white; text-align:center; margin-bottom:20px; font-size:16px; opacity:.7; }}
  .slides-container {{ display:flex; flex-direction:column; gap:20px; align-items:center; }}
  .slide {{
    width:600px; height:600px; border-radius:12px; position:relative;
    overflow:hidden; flex-shrink:0;
  }}
  .slide-inner {{ width:100%; height:100%; display:flex; flex-direction:column;
                  justify-content:center; align-items:center; padding:40px;
                  text-align:center; }}
  .slide-num {{
    position:absolute; bottom:14px; right:18px;
    color:rgba(255,255,255,0.5); font-size:12px;
  }}
  /* 제목 슬라이드 */
  .title-slide h1 {{
    color:white; font-size:32px; font-weight:800;
    line-height:1.5; margin-bottom:16px; text-shadow:0 2px 8px rgba(0,0,0,0.3);
  }}
  .subtitle {{ color:rgba(255,255,255,0.85); font-size:15px; margin-bottom:24px; }}
  .hsu-logo {{
    position:absolute; bottom:30px; left:50%; transform:translateX(-50%);
    color:white; font-size:14px; font-weight:700; opacity:.95;
    white-space:nowrap;
  }}
  /* 콘텐츠 슬라이드 */
  .content-slide {{ justify-content:flex-start; padding-top:28px; }}
  .label {{
    color:white; font-size:17px; font-weight:800;
    margin-bottom:14px; text-shadow:0 2px 6px rgba(0,0,0,0.3);
    letter-spacing:0.05em;
  }}
  .photo-box {{
    width:100%; height:230px; border:3px solid rgba(255,255,255,0.85);
    border-radius:8px; display:flex; align-items:center; justify-content:center;
    margin-bottom:14px; background:rgba(0,0,0,0.2);
  }}
  .photo-placeholder {{ color:rgba(255,255,255,0.6); font-size:14px; }}
  .body-text {{
    color:white; font-size:15px; line-height:1.9; text-align:center;
    text-shadow:0 1px 4px rgba(0,0,0,0.4);
    word-break:keep-all;
  }}
  .body-only {{ font-size:17px; margin-top:20px; line-height:2.0; }}
  .body-text strong {{ color:#FFD700; font-weight:800; }}
  .body-text em {{ color:#FFD700; font-style:normal; font-weight:700; }}

  /* 다운로드 버튼 */
  .download-btn {{
    display:block; margin:20px auto; padding:12px 32px;
    background:#C8001E; color:white; border:none; border-radius:8px;
    font-size:14px; font-weight:700; cursor:pointer; font-family:inherit;
  }}
  .download-btn:hover {{ opacity:.85; }}

  @media print {{
    body {{ background:white; padding:0; }}
    .slide {{ page-break-after:always; border-radius:0; }}
    .download-btn {{ display:none; }}
  }}
</style>
</head>
<body>
<h2>📋 {event_name} 카드뉴스 미리보기</h2>
<button class="download-btn" onclick="window.print()">🖨️ 인쇄 / PDF 저장</button>
<div class="slides-container">
{slides_html}
</div>
<button class="download-btn" onclick="window.print()">🖨️ 인쇄 / PDF 저장</button>
</body>
</html>'''
    return html

@cardnews_bp.route("/cardnews", methods=["POST"])
def generate_cardnews():
    data = request.json
    event_name      = data.get("event_name", "행사")
    event_org       = data.get("event_org", "")
    event_date      = data.get("event_date", "")
    event_place     = data.get("event_place", "")
    event_content   = data.get("event_content", "")
    event_attendees = data.get("event_attendees", "")

    system_prompt = load_prompt()
    user_message  = f"""
행사명: {event_name}
주관: {event_org}
일시: {event_date}
장소: {event_place}
참석자: {event_attendees}
주요내용: {event_content}

위 내용으로 카드뉴스 슬라이드를 생성해주세요.
반드시 JSON 형식만 출력하세요.
"""

    gpt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        max_tokens=2000,
    )

    raw = gpt_response.choices[0].message.content.strip()
    try:
        clean  = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
        result = json.loads(clean)
        slides = result.get("slides", [])
    except Exception as e:
        return respond({"error": f"파싱 실패: {str(e)}", "raw": raw}, 500)

    html = build_html(slides, event_name)
    return respond({"html": html, "slides": slides, "total": len(slides)})
