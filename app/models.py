# app/models.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    last_test_date = db.Column(db.DateTime, nullable=True)  # テスト実施日の追跡

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50), nullable=False)  # 問題の種類（例: 選択式, 記述式）
    text = db.Column(db.Text, nullable=False)  # 本文や設問
    correct_answer = db.Column(db.String(255), nullable=False)  # 正解
    choices = db.Column(db.String(1024), nullable=True)  # 選択肢（カンマ区切り）
    explanation = db.Column(db.Text, nullable=True)  # 解説や追加情報

    def get_choices(self):
        return self.choices.split(',') if self.choices else []


# 本文モデル
class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # 本文のタイトル
    content = db.Column(db.Text, nullable=False)  # 本文の内容
    questions = db.relationship('Question', backref='passage', lazy=True)  # 設問とのリレーション

# 設問モデル
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'), nullable=False)  # 本文への外部キー
    question_text = db.Column(db.Text, nullable=False)  # 設問の内容
    choices = db.Column(db.String(1024), nullable=True)  # 選択肢（カンマ区切り）
    correct_answer = db.Column(db.String(255), nullable=False)  # 正解
    question_type = db.Column(db.String(50), nullable=False, default="選択式")  # 問題の種類


class UserTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('test_results', lazy=True))