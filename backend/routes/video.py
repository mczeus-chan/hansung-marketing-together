from flask import Blueprint, request, Response, send_file
from dotenv import load_dotenv
import os, traceback, json, tempfile, requests
import fal_client
from moviepy import VideoFileClip, concatenate_videoclips

load_dotenv()
os.environ["FAL_KEY"] = os.environ.get("FAL_KEY", "")

video_bp = Blueprint("video", __name__)

def respond(data, code=200):
    return Response(
        json.dumps(data, ensure_ascii=True),
        status=code,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@video_bp.route("/upload-image", methods=["POST"])
def upload_image():
    try:
        print("[upload] request received", flush=True)
        if "file" not in request.files:
            return respond({"error": "no_file"}, 400)

        f = request.files["file"]
        img_bytes = f.read()
        print("[upload] file size=" + str(len(img_bytes)), flush=True)

        # fal_client.upload 사용
        url = fal_client.upload(img_bytes, "image/png")
        print("[upload] success url=" + str(url)[:80], flush=True)
        return respond({"url": url})

    except Exception as e:
        print("[upload] exception=" + str(e), flush=True)
        print(traceback.format_exc(), flush=True)
        return respond({"error": "exception"}, 500)

@video_bp.route("/video", methods=["POST"])
def generate_video():
    try:
        data   = json.loads(request.get_data(as_text=True))
        contis = data.get("contis", [])
        print("[video] contis=" + str(len(contis)), flush=True)

        if not contis:
            return respond({"error": "no_contis"}, 400)

        video_urls = []

        for c in sorted(contis, key=lambda x: x.get("conti_number", 0)):
            num   = c.get("conti_number", 0)
            s_url = c.get("start_url", "")
            e_url = c.get("end_url", "")
            pmt   = c.get("prompt", "")
            print("[video] conti=" + str(num), flush=True)

            if not s_url:
                continue

            try:
                payload = {
                    "image_url":    s_url,
                    "prompt":       (pmt or "smooth cinematic animation")[:300],
                    "duration":     "5",
                    "aspect_ratio": "9:16",
                    "cfg_scale":    0.5,
                }
                if e_url:
                    payload["tail_image_url"] = e_url

                result = fal_client.subscribe(
                    "fal-ai/kling-video/v1.6/standard/image-to-video",
                    arguments=payload
                )
                video_url = result.get("video", {}).get("url") or result.get("url")
                if video_url:
                    video_urls.append({"conti_number": num, "url": video_url})
                    print("[video] conti " + str(num) + " done", flush=True)

            except Exception as e:
                print("[video] conti " + str(num) + " error=" + str(e), flush=True)

        if not video_urls:
            return respond({"error": "no_videos_generated"}, 500)

        # 영상 다운로드 후 합치기
        print("[merge] downloading " + str(len(video_urls)) + " videos", flush=True)
        tmp_dir    = tempfile.mkdtemp()
        clip_paths = []

        for v in sorted(video_urls, key=lambda x: x["conti_number"]):
            r    = requests.get(v["url"], timeout=60)
            path = os.path.join(tmp_dir, "clip_" + str(v["conti_number"]) + ".mp4")
            with open(path, "wb") as f:
                f.write(r.content)
            clip_paths.append(path)
            print("[merge] downloaded conti " + str(v["conti_number"]), flush=True)

        print("[merge] concatenating", flush=True)
        clips  = [VideoFileClip(p) for p in clip_paths]
        final  = concatenate_videoclips(clips, method="compose")
        output = os.path.join(tmp_dir, "final_shortform.mp4")
        final.write_videofile(output, codec="libx264", audio=False, logger=None)

        for clip in clips:
            clip.close()
        final.close()
        print("[merge] done! " + output, flush=True)

        return send_file(
            output,
            mimetype="video/mp4",
            as_attachment=True,
            download_name="hansung_shortform.mp4"
        )

    except Exception as e:
        print("[video] exception=" + str(e), flush=True)
        print(traceback.format_exc(), flush=True)
        return respond({"error": "exception"}, 500)
