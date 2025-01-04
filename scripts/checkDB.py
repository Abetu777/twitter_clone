import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  Passage テーブルのデータを確認
from app.models import Passage, User
print(Passage.query.all())  # 全ての Passage データを確認
print(User.query.all())     # 全ての User データを確認
