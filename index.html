from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

press_bp = Blueprint("press", __name__)

# 프롬프트 파일 불러오기
def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/press_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

@press_bp.route("/press", methods=["POST"])
def generate_press():
    data = request.json
    dept_name   = data.get("dept_name", "")
    press_type  = data.get("press_type", "")
    summary     = data.get("summary", "")

    system_prompt = load_prompt()
    user_message = f"""
부서명: {dept_name}
행사·사업 유형: {press_type}
핵심 내용 요약: {summary}

위 내용을 바탕으로 보도자료를 작성해주세요.
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
