import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 仮のデータベース
posts = []

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Twitter Clone API!"

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "Invalid input"}), 400
    posts.append({"id": len(posts) + 1, "content": data["content"]})
    return jsonify(posts[-1]), 201

# 静的ファイルのホスティング
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
