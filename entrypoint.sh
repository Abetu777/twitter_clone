#!/bin/bash
# wait-for-db.shを使用して、DBが接続可能になるまで待機
echo "Waiting for the database to be available..."
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 1
done
echo "Database is up, starting the application..."
# アプリケーションの起動コマンドを実行
exec "$@"
