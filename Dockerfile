# ベースイメージ
FROM python:3.9-slim

# 必要なツールをインストール（ncを含む）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    netcat && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY . /app/

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r /app/requirements.txt

# Flaskアプリの環境変数を設定
ENV FLASK_APP=app.main
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# エントリーポイントスクリプトを実行可能にする
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ポートの指定（Flaskのデフォルトポート）
EXPOSE 5000

# エントリーポイントを設定
ENTRYPOINT ["/entrypoint.sh"]

# Flaskアプリケーションを起動
CMD ["gunicorn", "app.main:app", "--chdir", "/app", "--bind", "0.0.0.0:5000", "--workers", "3"]
