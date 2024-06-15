from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.inline.rating_kbs import rating_main_kb, rating_books_kb, back_rating_main
from loader import db

router = Router()


@router.message(F.text == "📊 Reyting")
async def router_main(message: types.Message,  state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = await db.select_user(
        telegram_id=user_id
    )
    if user:
        await message.answer(
            text="Reyting turini tanlang", reply_markup=rating_main_kb()
        )
    else:
        await message.answer(
            text="Ma'lumotlaringiz foydalanuvchilar ro'yxatidan topilmadi! Iltimos, /start buyrug'ini kiritib qayta "
                 "urinib ko'ring"
        )


@router.callback_query(F.data == "back_rating_main")
async def rating_by_book(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Reyting turini tanlang", reply_markup=rating_main_kb()
    )


@router.callback_query(F.data == "rating_overall")
async def rating_overall(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    rating_overall_ = await db.get_rating_all_()
    overall_text = str()
    user_rating = int()
    for index, rating in enumerate(rating_overall_):
        index = index + 1
        user = await db.select_user(
            telegram_id=rating['telegram_id']
        )
        try:
            if index <= 20:
                if user['telegram_id'] == telegram_id:
                    user_rating = index
                overall_text += f"{index}) {user['full_name']} - {rating['total_result']} ball\n"
            else:
                user_rating += index
        except Exception as err:
            await callback_query.message.answer(
                text=f"{err}"
            )
    await callback_query.message.edit_text(
        text=f"Umumiy reyting.\nTOP 20:\n\n{overall_text}\n<b>Umumiy reytingda Siz {user_rating} - o'rindasiz!</b>"
             f"\n\n<i>* Izoh:\nMabodo boshqa ishtirokchilar bilan to'plagan ballaringiz bir xil lekin o'rinlar xar "
             f"hil bo'lsa, bot eng kam vaqt sarflab, eng ko'p to'g'ri javob bergan ishtirokchini yuqoriroq o'ringa "
             f"qo'yadi!</i>",
        reply_markup=back_rating_main
    )


@router.callback_query(F.data == "rating_by_book")
async def rating_by_book(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Kerakli kitobni tanlang", reply_markup=await rating_books_kb()
    )


@router.callback_query(F.data.startswith("rating:"))
async def get_rating_book(callback_query: types.CallbackQuery):
    telegram_id = int(callback_query.from_user.id)
    book_id = int(callback_query.data.split(":")[1])
    rating_text = str()
    user_rating = int()
    get_book = await db.select_book_by_id(
        id_=book_id
    )
    get_rating_by_book = await db.get_rating_book(
        book_id=book_id
    )
    book_name = get_book['table_name']
    for index, rating in enumerate(get_rating_by_book):
        index = index + 1
        user = await db.select_user(
            telegram_id=rating['telegram_id']
        )
        if index <= 20:
            if user['telegram_id'] == telegram_id:
                user_rating = index
            rating_text += f"{index}) {user['full_name']} - {rating['result']} ball\n"
        else:
            user_rating += index

    await callback_query.message.edit_text(
        text=f"{book_name} kitobi bo'yicha reyting.\nTOP 20:\n\n{rating_text}"
             f"\n<b>{book_name} kitobi reytingida Siz {user_rating} - o'rindasiz!</b>"
             f"\n\n<i>* Izoh:\nMabodo boshqa ishtirokchilar bilan to'plagan ballaringiz bir xil lekin o'rinlar xar "
             f"hil bo'lsa, bot eng kam vaqt sarflab, eng ko'p to'g'ri javob bergan ishtirokchini yuqoriroq o'ringa "
             f"qo'yadi!</i>",
        reply_markup=back_rating_main
    )
