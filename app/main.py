import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 仮のデータベース
posts = []

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render用にポートを動的に設定
    app.run(host="0.0.0.0", port=port)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Twitter Clone API!"