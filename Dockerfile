# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY app/ /app/
COPY entrypoint.sh /entrypoint.sh

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリの環境変数を設定
ENV FLASK_APP=/app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# エントリーポイントスクリプトを実行可能にする
RUN chmod +x /entrypoint.sh

# ポートの指定（Flaskのデフォルトポート）
EXPOSE 5000

# エントリーポイントを設定
ENTRYPOINT ["/entrypoint.sh"]

# Flaskアプリケーションを起動
CMD ["gunicorn", "main:app", "--chdir", "/app", "--bind", "0.0.0.0:5000", "--workers", "3"]
