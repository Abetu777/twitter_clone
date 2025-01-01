import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースモデル
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# データベース初期化
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Twitter Clone API!"

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "content": post.content} for post in posts])

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_post = Post(content=data["content"])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"id": new_post.id, "content": new_post.content}), 201

# 静的ファイルのホスティング
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
