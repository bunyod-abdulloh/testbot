from aiogram import Router, types, F

from keyboards.inline.rating_kbs import rating_main_kb
from loader import db

router = Router()


# async def nimadir(book_id, telegram_id):
#     # To'g'ri javoblar soni
#     correct_answers = await db.count_answers(
#         telegram_id=telegram_id, answer="✅"
#     )
#     # Noto'g'ri javoblar soni
#     wrong_answers = await db.count_answers(
#         telegram_id=telegram_id, answer="❌"
#     )
#     # Results jadvalidan user reytingini kitob bo'yicha aniqlash
#     rating_book = await db.get_rating_by_result(
#         book_id=book_id
#     )
#
#     rating_book_ = int()
#     book_points = int()
#
#     for index, result in enumerate(rating_book):
#         if result['telegram_id'] == telegram_id:
#             rating_book_ += index + 1
#             book_points += result['result']
#             break
#
#     # Results jadvalidan userning umumiy reytingini aniqlash
#     all_rating = await db.get_rating_all()
#     all_rating_ = int()
#     all_points = int()
#     for index, result in enumerate(all_rating):
#         if result['telegram_id'] == telegram_id:
#             all_rating_ += index + 1
#             all_points += result['result']
#             break
#     # Results jadvalidan raqib reytingini kitob bo'yicha aniqlash
#     second_rating_book = int()
#     second_points = int()
#     for index, result in enumerate(rating_book):
#         if result['telegram_id'] == second_telegram_id:
#             second_rating_book += index + 1
#             second_points += result['result']
#             break
#     # Results jadvalidan raqib umumiy reytingini aniqlash
#     second_all_rating = int()
#     second_all_points = int()
#     for index, result in enumerate(all_rating):
#         if result['telegram_id'] == second_telegram_id:
#             second_all_rating += index + 1
#             second_all_points += result['result']
#             break
#     rating_book = await db.get_rating_by_result(
#         book_id=book_id
#     )
#     first_rating_book_ = int()
#     first_points = int()
#     for index, result in enumerate(rating_book):
#         if result['telegram_id'] == first_telegram_id:
#             first_rating_book_ += index + 1
#             first_points += result['result']
#             break
#     # Results jadvalidan userning umumiy reytingini aniqlash
#     all_rating = await db.get_rating_all()
#     first_all_rating = int()
#     first_all_points = int()
#     for index, result in enumerate(all_rating):
#         if result['telegram_id'] == first_telegram_id:
#             first_all_rating += index + 1
#             first_all_points += result['result']
#             break

@router.message(F.text == "📊 Reyting")
async def router_main(message: types.Message):
    await message.answer(
        text="Reyting turini tanlang", reply_markup=rating_main_kb()
    )


@router.callback_query(F.data == "back_rating_main")
async def rating_by_book(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Reyting turini tanlang", reply_markup=rating_main_kb()
    )


@router.callback_query(F.data == "rating_overall")
async def rating_overall(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    rating_overall_ = await db.get_rating_all()
    overall_text = str()
    for index, rating in enumerate(rating_overall_):
        overall_text += f"{index + 1}) {rating['result']}\n"
