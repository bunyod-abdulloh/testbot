import random

from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


async def get_builder(book_id):
    questions = await db.select_all_questions(table_name=f"table_{book_id}")
    question_id = questions[0]['id']
    letters = ["A", "B", "C", "D"]

    a = ["a", f"{questions[0]['a_correct']}"]
    b = ["b", f"{questions[0]['b']}"]
    c = ["c", f"{questions[0]['c']}"]
    d = ["d", f"{questions[0]['d']}"]

    answers = [a, b, c, d]
    random.shuffle(answers)
    questions_text = str()

    for letter, question in zip(letters, answers):
        questions_text += f"{letter}) {question[1]}\n"

    builder = InlineKeyboardBuilder()
    return question_id, questions_text, letters, answers, builder, questions
