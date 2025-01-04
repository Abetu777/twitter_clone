import sys
import os

# プロジェクトのルートディレクトリを `sys.path` に追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models import Test

from app import create_app, db

app = create_app()

with app.app_context():
    questions = [
        {
            "question_type": "選択式",
            "text": "春に行われる「花見」の特徴として正しいものを選べ",
            "choices": "桜を鑑賞するだけでなく、人々が集まり語らう機会でもある,夜空に咲く大輪の花火を楽しむ行事である,山々の紅葉を眺めながら自然を感じる行事である,家族でこたつに入りながら語らう時間である",
            "correct_answer": "桜を鑑賞するだけでなく、人々が集まり語らう機会でもある",
            "explanation": "春の花見は桜を見るだけでなく、人々が集い交流する文化的イベントです。",
        },
        {
            "question_type": "選択式",
            "text": "本文中で「夏」の文化として挙げられているものはどれか",
            "choices": "花見と月見,花火大会と祭り,紅葉狩りと初詣,おせち料理と雪景色",
            "correct_answer": "花火大会と祭り",
            "explanation": "夏の代表的な文化は花火大会と祭りで、全国各地で行われます。",
        },
        {
            "question_type": "選択式",
            "text": "「日本の四季」の文化の特徴として本文に述べられていないものはどれか",
            "choices": "秋の紅葉狩り,冬の雪景色とこたつ,春の新しい出会いの象徴,夏の避暑地でのバカンス",
            "correct_answer": "夏の避暑地でのバカンス",
            "explanation": "本文では避暑地でのバカンスについては触れられていません。",
        },
    ]

    for q in questions:
        if not Test.query.filter_by(text=q["text"]).first():
            new_question = Test(
                question_type=q["question_type"],
                text=q["text"],
                choices=q["choices"],
                correct_answer=q["correct_answer"],
                explanation=q.get("explanation", ""),
            )
            db.session.add(new_question)

    db.session.commit()
    print("Questions added successfully.")
