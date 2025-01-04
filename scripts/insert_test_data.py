from app.models import db, Test
from app import create_app

app = create_app()

with app.app_context():
    test_questions = [
        {"question": "What is 2+2?", "correct_answer": "4", "choices": "1,2,3,4"},
        {"question": "What is the capital of France?", "correct_answer": "Paris", "choices": "London,Paris,Rome,Berlin"},
    ]
    for q in test_questions:
        if not Test.query.filter_by(question=q["question"]).first():
            new_test = Test(question=q["question"], correct_answer=q["correct_answer"], choices=q["choices"])
            db.session.add(new_test)
    db.session.commit()
