# app/main.py
import os
from flask_migrate import upgrade, init, migrate
import sys
import os

# プロジェクトのルートディレクトリを `sys.path` に追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

app = create_app()

# マイグレーションの実行
with app.app_context():
    # Migrationsフォルダの存在を確認
    if not os.path.exists(os.path.join(os.getcwd(), 'migrations')):
        print("Migrations folder not found. Initializing...")
        init()  # Migrationsフォルダを初期化
        migrate(message="Initial migration")  # マイグレーションスクリプトを生成
    print("Applying migrations...")
    upgrade()  # マイグレーションを適用
    print("Database migration applied successfully.")

# アプリケーションの起動
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
