# app/routes.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db, bcrypt
from app.models import User, Post, Test, UserTestResult, Passage
from datetime import datetime

bp = Blueprint("routes", __name__)

# ホームページ
@bp.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("routes.dashboard"))
    return render_template("index.html")

# ダッシュボード
@bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("routes.login_page"))

    user = User.query.get(session["user_id"])
    posts = Post.query.order_by(Post.id.desc()).all()
    last_result = UserTestResult.query.filter_by(user_id=user.id).order_by(UserTestResult.created_at.desc()).first()

    return render_template("dashboard.html", posts=posts, score=last_result.score if last_result else None)

# ユーザー登録
@bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        data = request.form
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # 登録後にテストページへリダイレクト
        session['user_id'] = new_user.id
        return redirect(url_for("routes.take_test"))  # テストページへリダイレクト
    return render_template("register.html")

# ログイン
@bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            return redirect(url_for("routes.dashboard"))
        return jsonify({"error": "Invalid credentials"}), 401
    return render_template("login.html")

# ログアウト
@bp.route("/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for("routes.home"))

# 投稿作成
@bp.route("/create_post", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.form
    if not data.get("content"):
        return jsonify({"error": "Content cannot be empty"}), 400
    new_post = Post(content=data["content"], user_id=session["user_id"])
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("routes.dashboard"))

@bp.route("/take_test", methods=["GET", "POST"])
def take_test():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session["user_id"])

    if request.method == "GET":
        # ランダムに1つのパッセージを取得
        passage = Passage.query.order_by(db.func.random()).first()
        if not passage:
            return jsonify({"error": "No passages available"}), 404

        # パッセージ詳細ページにリダイレクト
        return redirect(url_for("routes.read_passage", passage_id=passage.id))

    if request.method == "POST":
        # POSTは不要なら削除する
        return jsonify({"message": "POST method not implemented"}), 405


@bp.route("/test_result")
def test_result():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session["user_id"])
    last_result = UserTestResult.query.filter_by(user_id=user.id).order_by(UserTestResult.created_at.desc()).first()

    return render_template("test_result.html", score=last_result.score, date=last_result.created_at)

@bp.route("/passages", methods=["GET"])
def list_passages():
    passages = Passage.query.all()
    return render_template("passage.html", passages=passages)

@bp.route("/read_passage/<int:passage_id>", methods=["GET", "POST"])
def read_passage(passage_id):
    passage = Passage.query.get_or_404(passage_id)

    if request.method == "POST":
        data = request.form
        questions = passage.questions
        score = sum(1 for q in questions if data.get(str(q.id)) == q.correct_answer)
        return render_template("result.html", score=score, total=len(questions))

    return render_template("passage.html", passage=passage)



