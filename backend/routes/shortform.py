from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

shortform_bp = Blueprint("shortform", __name__)

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/shortform_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

@shortform_bp.route("/shortform", methods=["POST"])
def generate_shortform():
    data = request.json
    topic  = data.get("topic", "")
    mood   = data.get("mood", "역동적·에너지")
    engine = data.get("engine", "Kling AI")

    system_prompt = load_prompt()
    user_message = f"""
주제: {topic}
분위기: {mood}
사용 영상 생성 엔진: {engine}

위 조건으로 5개 콘티를 작성해주세요.
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
