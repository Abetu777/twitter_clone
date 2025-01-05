#!/bin/bash
# entrypoint.sh の例

# PostgreSQL に接続するための待機処理
echo "Waiting for database connection..."
while ! nc -z db 5432; do
  sleep 1
done

# Flask アプリケーションの起動
exec gunicorn app.main:app --bind 0.0.0.0:5000
