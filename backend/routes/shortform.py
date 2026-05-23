from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

shortform_bp = Blueprint("shortform", __name__)

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/shortform_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

@shortform_bp.route("/shortform", methods=["POST"])
def generate_shortform():
    data    = request.json
    topic   = data.get("topic", "")
    mood    = data.get("mood", "역동적·에너지")
    contis  = data.get("contis", [])  # 각 콘티별 컨셉 입력값

    system_prompt = load_prompt()

    # 콘티 컨셉 정리
    conti_text = ""
    for i, c in enumerate(contis):
        concept = c.get("concept", "").strip()
        if concept:
            conti_text += f"콘티 {i+1}: {concept}\n"
        else:
            conti_text += f"콘티 {i+1}: (자유롭게 구성)\n"

    user_message = f"""
주제: {topic}
분위기: {mood}

각 콘티 컨셉:
{conti_text}

위 컨셉을 기반으로 각 콘티의 시작·종료 이미지 프롬프트를 작성해주세요.
반드시 JSON 배열 형식만 출력하세요. 다른 텍스트는 절대 포함하지 마세요.
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
    except Exception as e:
        return json.dumps({"error": f"파싱 실패: {str(e)}", "raw": raw}, ensure_ascii=False), 500

    return json.dumps({"contis": result}, ensure_ascii=False), 200, {"Content-Type": "application/json"}
