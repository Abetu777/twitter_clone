# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

# 拡張機能の初期化
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # データベース設定: PostgreSQL (本番) または SQLite (ローカル)
    if os.getenv("DATABASE_URL"):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../instance/app.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # インスタンスフォルダの作成
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)

    # 拡張機能の初期化
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # ルーティングの登録
    from app.routes import bp
    app.register_blueprint(bp)

    return app
