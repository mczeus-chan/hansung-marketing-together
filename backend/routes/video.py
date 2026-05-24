from flask import Blueprint, request, Response
from dotenv import load_dotenv
import os, requests, traceback, json, base64

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
    headers = {"Authorization": f"Key {FAL_KEY}"}
    files   = {"file": ("image.png", file_bytes, "image/png")}
    r = requests.post(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        headers=headers, files=files, timeout=60
    )
    if r.status_code != 200:
        # fallback to direct upload
        r = requests.post(
            "https://fal.run/files",
            headers=headers, files=files, timeout=60
        )
    print(f"[upload] status={r.status_code}", flush=True)
    if r.status_code == 200:
        d = r.json()
        return d.get("url") or d.get("file_url")
    print(f"[upload] error={r.text[:100]}", flush=True)
    return None

def make_video(start_url, end_url, prompt):
    headers = {
        "Authorization": f"Key {FAL_KEY}",
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

    print(f"[video] kling request start", flush=True)
    r = requests.post(
        "https://fal.run/fal-ai/kling-video/v1.6/standard/image-to-video",
        headers=headers, json=payload, timeout=300
    )
    print(f"[video] kling status={r.status_code}", flush=True)
    if r.status_code != 200:
        return None, f"kling_error_{r.status_code}"
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
        print(f"[upload] file size={len(img_bytes)}", flush=True)
        url = upload_to_fal(img_bytes)
        if url:
            print(f"[upload] success url={url[:50]}", flush=True)
            return respond({"url": url})
        return respond({"error": "upload_failed"}, 500)
    except Exception as e:
        print(f"[upload] exception={str(e)}", flush=True)
        return respond({"error": "exception"}, 500)

@video_bp.route("/video", methods=["POST"])
def generate_video():
    try:
        data   = json.loads(request.get_data(as_text=True))
        contis = data.get("contis", [])
        mood   = data.get("mood", "역동적·에너지")
        print("[video] mood=" + mood, flush=True)
        print(f"[video] contis={len(contis)}", flush=True)
        if not contis:
            return respond({"error": "no_contis"}, 400)

        results = []
        for c in contis:
            num   = c.get("conti_number", 0)
            s_url = c.get("start_url", "")
            e_url = c.get("end_url", "")
            pmt   = c.get("prompt", "")
            print(f"[video] conti={num}", flush=True)
            if not s_url:
                results.append({"conti_number": num, "video_url": None, "error": "no_url"})
                continue
            video_url, error = make_video(s_url, e_url, pmt)
            results.append({"conti_number": num, "video_url": video_url, "error": error})

        return respond({"videos": results, "total": len(results)})
    except Exception as e:
        print(f"[video] exception={str(e)}", flush=True)
        return respond({"error": "exception"}, 500)
