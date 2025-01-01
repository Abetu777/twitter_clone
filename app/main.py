from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_migrate import Migrate, init, migrate, upgrade
import os


# Flaskアプリケーション初期化
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# データベース設定: PostgreSQL (本番) または SQLite (ローカル)
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../instance/app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLite用ディレクトリの確認と作成 (ローカル環境用)
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

# データベースとBcryptの初期化
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask-Migrateの初期化
migrate = Migrate(app, db)

# データベースモデル定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Render環境でのマイグレーションフォルダの確認と初期化
try:
    with app.app_context():
        migrations_path = os.path.join(os.getcwd(), 'migrations')
        if not os.path.exists(migrations_path):
            print("Migrations folder not found. Initializing...")
            init()
            migrate(message="Initial migration")
        upgrade()
        print("Database migration applied successfully.")
except Exception as e:
    print(f"Error applying migrations: {e}")

# ホームページ
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# ダッシュボード
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    posts = Post.query.order_by(Post.id.desc()).all()
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

# アプリケーション起動
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
