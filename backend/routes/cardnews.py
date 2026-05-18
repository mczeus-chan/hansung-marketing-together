from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

cardnews_bp = Blueprint("cardnews", __name__)

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/cardnews_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

@cardnews_bp.route("/cardnews", methods=["POST"])
def generate_cardnews():
    data = request.json
    event_name      = data.get("event_name", "")
    event_org       = data.get("event_org", "")
    event_date      = data.get("event_date", "")
    event_place     = data.get("event_place", "")
    event_content   = data.get("event_content", "")
    event_attendees = data.get("event_attendees", "")

    system_prompt = load_prompt()
    user_message = f"""
행사명: {event_name}
주관 부서·단체: {event_org}
일시: {event_date}
장소: {event_place}
참석자: {event_attendees}
주요 내용: {event_content}

위 내용으로 4슬라이드 카드뉴스를 작성해주세요.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        max_tokens=1500,
    )

    result = response.choices[0].message.content
    return jsonify({"result": result})
