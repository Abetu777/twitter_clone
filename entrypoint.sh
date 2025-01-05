#!/bin/bash

# 環境変数に基づいてデータベースURIを設定
if [ "$FLASK_ENV" = "production" ]; then
  echo "Running in production mode"
  export DATABASE_URL=${DATABASE_URL:-"postgresql://user:password@db:5432/production_db"}
else
  echo "Running in development mode"
  export DATABASE_URL="sqlite:///../instance/app.db"
fi

# マイグレーションを実行
flask db upgrade || echo "Database already upgraded"

# Flaskアプリケーションを起動
exec "$@"