# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY . /app/

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリの環境変数を設定
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# ポートの指定（Flaskのデフォルトポート）
EXPOSE 5000

# コンテナ起動時にマイグレーションを実行
RUN flask db upgrade || echo "Database already upgraded"

# Flaskアプリケーションをgunicornで起動
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers", "3"]
