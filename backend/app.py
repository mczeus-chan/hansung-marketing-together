from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.press import press_bp
from routes.shortform import shortform_bp
from routes.cardnews import cardnews_bp
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# API 라우트 등록
app.register_blueprint(press_bp, url_prefix="/api")
app.register_blueprint(shortform_bp, url_prefix="/api")
app.register_blueprint(cardnews_bp, url_prefix="/api")

# 프론트엔드 서빙
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True") == "True"
    print(f"서버 시작: http://localhost:{port}")
    app.run(port=port, debug=debug)
