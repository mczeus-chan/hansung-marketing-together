# -*- coding: utf-8 -*-
"""
한성 마케팅투게더 - 파일 자동 생성 스크립트
이 파일을 backend 폴더에서 실행하세요: python setup.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

# ── app.py ──────────────────────────────────────────
write("app.py", """import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.press import press_bp
from routes.shortform import shortform_bp
from routes.cardnews import cardnews_bp
from routes.video import video_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

app.register_blueprint(press_bp, url_prefix="/api")
app.register_blueprint(shortform_bp, url_prefix="/api")
app.register_blueprint(cardnews_bp, url_prefix="/api")
app.register_blueprint(video_bp, url_prefix="/api")

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True") == "True"
    print("server start: http://localhost:" + str(port))
    app.run(port=port, debug=debug)
""")

# ── routes/video.py ─────────────────────────────────
write("routes/video.py", """from flask import Blueprint, request, Response
from dotenv import load_dotenv
import os, requests, traceback, json

load_dotenv()
FAL_KEY = os.environ.get("FAL_KEY", "")
video_bp = Blueprint("video", __name__)

def respond(data, code=200):
    return Response(
        json.dumps(data, ensure_ascii=True),
        status=code,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

def upload_to_fal(file_bytes):
    headers = {"Authorization": "Key " + FAL_KEY}
    files   = {"file": ("image.png", file_bytes, "image/png")}
    r = requests.post(
        "https://fal.run/files/upload",
        headers=headers, files=files, timeout=60
    )
    print("[upload] status=" + str(r.status_code), flush=True)
    if r.status_code == 200:
        d = r.json()
        return d.get("url") or d.get("file_url")
    print("[upload] error=" + r.text[:100], flush=True)
    return None

def make_video(start_url, end_url, prompt):
    headers = {
        "Authorization": "Key " + FAL_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "image_url":    start_url,
        "prompt":       (prompt or "smooth cinematic animation")[:300],
        "duration":     "5",
        "aspect_ratio": "9:16",
        "cfg_scale":    0.5,
    }
    if end_url:
        payload["tail_image_url"] = end_url

    print("[video] kling request start", flush=True)
    r = requests.post(
        "https://fal.run/fal-ai/kling-video/v1.6/standard/image-to-video",
        headers=headers, json=payload, timeout=300
    )
    print("[video] kling status=" + str(r.status_code), flush=True)
    if r.status_code != 200:
        return None, "kling_error_" + str(r.status_code)
    result = r.json()
    url = result.get("video", {}).get("url") or result.get("url")
    return url, None

@video_bp.route("/upload-image", methods=["POST"])
def upload_image():
    try:
        print("[upload] request received", flush=True)
        if "file" not in request.files:
            return respond({"error": "no_file"}, 400)
        f = request.files["file"]
        img_bytes = f.read()
        print("[upload] file size=" + str(len(img_bytes)), flush=True)
        url = upload_to_fal(img_bytes)
        if url:
            print("[upload] success", flush=True)
            return respond({"url": url})
        return respond({"error": "upload_failed"}, 500)
    except Exception as e:
        print("[upload] exception=" + str(e), flush=True)
        return respond({"error": "exception"}, 500)

@video_bp.route("/video", methods=["POST"])
def generate_video():
    try:
        data   = json.loads(request.get_data(as_text=True))
        contis = data.get("contis", [])
        print("[video] contis=" + str(len(contis)), flush=True)
        if not contis:
            return respond({"error": "no_contis"}, 400)

        results = []
        for c in contis:
            num   = c.get("conti_number", 0)
            s_url = c.get("start_url", "")
            e_url = c.get("end_url", "")
            pmt   = c.get("prompt", "")
            print("[video] conti=" + str(num), flush=True)
            if not s_url:
                results.append({"conti_number": num, "video_url": None, "error": "no_url"})
                continue
            video_url, error = make_video(s_url, e_url, pmt)
            results.append({"conti_number": num, "video_url": video_url, "error": error})

        return respond({"videos": results, "total": len(results)})
    except Exception as e:
        print("[video] exception=" + str(e), flush=True)
        return respond({"error": "exception"}, 500)
""")

print("")
print("=== 완료! ===")
print("이제 python app.py 를 실행하세요.")
