from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Flaskアプリケーション初期化
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# データベースモデル定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# データベース初期化
with app.app_context():
    db.create_all()

# ホームページ
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# ダッシュボード（ログインユーザー専用）
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    user_id = session["user_id"]
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("dashboard.html", posts=posts)

# ユーザー登録
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        data = request.form
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login_page"))
    return render_template("register.html")

# ログイン
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            return redirect(url_for("dashboard"))
        return jsonify({"error": "Invalid credentials"}), 401
    return render_template("login.html")

# ログアウト
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for("home"))

# 投稿作成
@app.route("/create_post", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.form
    if not data.get("content"):
        return jsonify({"error": "Content cannot be empty"}), 400
    new_post = Post(content=data["content"], user_id=session["user_id"])
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
