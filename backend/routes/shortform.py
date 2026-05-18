from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
import base64

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

shortform_bp = Blueprint("shortform", __name__)

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/shortform_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

SANGSANG_BUGI_BASE = (
    "a cute chubby 3D clay-rendered turtle character named Sangsang Bugi, "
    "wearing a navy blue hoodie with 'HSU' text on the chest and a small white bow tie at the collar, "
    "round white face with small black dot eyes, light blue rosy cheeks, small curved mouth, "
    "wavy navy eyebrows, white turtle shell visible on the back sticking out from the hoodie, "
    "stubby white hands and feet, matte clay texture, soft toy figure aesthetic, "
    "Pixar-style 3D character rendering, clean and friendly appearance"
)

FRIENDS_PROMPTS = {
    "white chicken": (
        "a cute 3D clay-rendered white chicken character, "
        "red comb on head, navy blue bow tie, round blue eyes, "
        "plump round white body, flat stubby wings and feet, "
        "matte clay texture, same Pixar-style 3D as Sangsang Bugi"
    ),
    "brown chicken": (
        "a cute 3D clay-rendered brown chicken character, "
        "small pink comb, yellow neck scarf, round expressive eyes, "
        "chubby brown body with fluffy wing texture, "
        "matte clay texture, same Pixar-style 3D as Sangsang Bugi"
    ),
    "cat": (
        "a cute 3D clay-rendered white cat character, "
        "pink ears and tail, wearing a white HSU t-shirt, "
        "carrying a brown turtle-shell shaped backpack, "
        "navy blue whisker lines and eyebrows, round expressive eyes, "
        "matte clay texture, same Pixar-style 3D as Sangsang Bugi"
    ),
    "frog": (
        "a cute small 3D clay-rendered green frog character, "
        "light yellow-green belly, small round eyes, tiny cute body, "
        "matte clay texture, same Pixar-style 3D as Sangsang Bugi"
    ),
}

STYLE_SUFFIX = (
    "9:16 vertical frame, 3D clay render, Pixar-style, "
    "soft matte texture, cinematic lighting, high quality, professional 3D render"
)

def build_full_prompt(prompt, friends):
    if "Sangsang Bugi" not in prompt:
        prompt = SANGSANG_BUGI_BASE + ", " + prompt
    if friends:
        friend_descs = []
        for f in friends:
            key = f.lower().strip()
            if key in FRIENDS_PROMPTS:
                friend_descs.append(FRIENDS_PROMPTS[key])
        if friend_descs:
            prompt += ", alongside " + " and ".join(friend_descs)
    return f"{prompt}, {STYLE_SUFFIX}"

def generate_image(prompt, friends, conti_num, image_type):
    try:
        full_prompt = build_full_prompt(prompt, friends)
        response = client.images.generate(
            model="gpt-image-1",
            prompt=full_prompt,
            size="1024x1536",
            quality="medium",
            n=1,
        )
        image_b64 = response.data[0].b64_json
        image_url = f"data:image/png;base64,{image_b64}"
        return {
            "conti_number": conti_num,
            "image_type": image_type,
            "url": image_url,
            "prompt": full_prompt,
        }
    except Exception as e:
        return {
            "conti_number": conti_num,
            "image_type": image_type,
            "url": None,
            "error": str(e),
        }

@shortform_bp.route("/shortform", methods=["POST"])
def generate_shortform():
    data = request.json
    topic = data.get("topic", "")
    mood  = data.get("mood", "역동적·에너지")

    system_prompt = load_prompt()
    user_message = f"""
주제: {topic}
분위기: {mood}

위 조건으로 5개 콘티를 작성해주세요.
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
        clean = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
        contis = json.loads(clean)
    except Exception as e:
        return jsonify({"error": f"콘티 파싱 실패: {str(e)}", "raw": raw}), 500

    images = []
    for conti in contis:
        num     = conti.get("conti_number", 0)
        friends = conti.get("friends", [])

        start = generate_image(conti.get("start_image_prompt", ""), friends, num, "start")
        start["title"]       = conti.get("title", "")
        start["description"] = conti.get("description", "")
        start["friends"]     = friends
        images.append(start)

        end = generate_image(conti.get("end_image_prompt", ""), friends, num, "end")
        end["title"]       = conti.get("title", "")
        end["description"] = conti.get("description", "")
        end["friends"]     = friends
        images.append(end)

    return jsonify({
        "contis": contis,
        "images": images,
        "total": len(images),
    })
