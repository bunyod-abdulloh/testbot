from aiogram import Router, types, F

from loader import db

router = Router()


async def nimadir(book_id, telegram_id):
    # To'g'ri javoblar soni
    correct_answers = await db.count_answers(
        telegram_id=telegram_id, answer="✅"
    )
    # Noto'g'ri javoblar soni
    wrong_answers = await db.count_answers(
        telegram_id=telegram_id, answer="❌"
    )
    # Results jadvalidan user reytingini kitob bo'yicha aniqlash
    rating_book = await db.get_rating_by_result(
        book_id=book_id
    )

    rating_book_ = int()
    book_points = int()

    for index, result in enumerate(rating_book):
        if result['telegram_id'] == telegram_id:
            rating_book_ += index + 1
            book_points += result['result']
            break

    # Results jadvalidan userning umumiy reytingini aniqlash
    all_rating = await db.get_rating_all()
    all_rating_ = int()
    all_points = int()
    for index, result in enumerate(all_rating):
        if result['telegram_id'] == telegram_id:
            all_rating_ += index + 1
            all_points += result['result']
            break


@router.message(F.text == "📊 Reyting")
async def router_main(message: types.Message):
    pass
