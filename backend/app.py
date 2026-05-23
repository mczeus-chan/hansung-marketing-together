import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.press import press_bp
from routes.shortform import shortform_bp
from routes.cardnews import cardnews_bp
from routes.video import video_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
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