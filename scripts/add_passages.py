import sys
import os
# プロジェクトのルートディレクトリを `sys.path` に追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models import Passage, Question
from app import create_app, db

app = create_app()

with app.app_context():
    passages = [
        {
            "title": "日本の四季と文化",
            "content": """日本には四季があり、それぞれが独特の風景と文化を形成している...""",
            "questions": [
                {
                    "question_text": "春に行われる「花見」の特徴として正しいものを選べ",
                    "choices": "桜を鑑賞するだけでなく、人々が集まり語らう機会でもある,夜空に咲く大輪の花火を楽しむ行事である,山々の紅葉を眺めながら自然を感じる行事である,家族でこたつに入りながら語らう時間である",
                    "correct_answer": "桜を鑑賞するだけでなく、人々が集まり語らう機会でもある",
                },
                {
                    "question_text": "本文中で「夏」の文化として挙げられているものはどれか",
                    "choices": "花見と月見,花火大会と祭り,紅葉狩りと初詣,おせち料理と雪景色",
                    "correct_answer": "花火大会と祭り",
                },
            ]
        },
        {
            "title": "環境問題と持続可能性",
            "content": """環境問題は現代社会が直面する最大の課題の一つであり...""",
            "questions": [
                {
                    "question_text": "持続可能な開発とは何を目指すものか？",
                    "choices": "経済成長のみ,環境保護のみ,経済成長と環境保護の両立,資源の枯渇",
                    "correct_answer": "経済成長と環境保護の両立",
                },
                {
                    "question_text": "温暖化の主な原因とされるものはどれか？",
                    "choices": "水蒸気,二酸化炭素,メタンガス,酸素",
                    "correct_answer": "二酸化炭素",
                },
            ]
        },
    ]

    for passage_data in passages:
        passage = Passage(title=passage_data["title"], content=passage_data["content"])
        db.session.add(passage)
        db.session.commit()

        for q_data in passage_data["questions"]:
            question = Question(
                passage_id=passage.id,
                question_text=q_data["question_text"],
                choices=q_data["choices"],
                correct_answer=q_data["correct_answer"]
            )
            db.session.add(question)

    db.session.commit()
    print("Passages and questions added successfully.")
