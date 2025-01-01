# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY app/ /app/

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r /app/requirements.txt

# ポートの指定（Flaskのデフォルトポート）
EXPOSE 5000

# Flaskアプリケーションを起動
CMD ["python", "main.py"]
