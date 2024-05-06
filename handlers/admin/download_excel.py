from aiogram import Router, types, F

from handlers.admin.main import books_menu
from loader import db
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel

router = Router()

admin = int(ADMINS[0])


@router.message(F.text == 'Excel shaklda yuklab olish', IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    await message.answer(
        text="Kerakli kitobni tanlang", reply_markup=await books_menu(
            callback_text="download_book"
        )
    )


@router.callback_query(F.data.startswith("download_book:"))
async def download_book(call: types.CallbackQuery):
    kitob_id = int(call.data.split(":")[1])
    kitob_nomi = await db.select_book_by_id(
        id_=kitob_id
    )
    all_questions = await db.select_all_questions_(
        table_name=f"table_{kitob_id}"
    )
    kitob_nomi_ = kitob_nomi['table_name'].replace("|", "_").replace(" ", "_")
    file_path = f"downloads/documents/{kitob_nomi_}.xlsx"
    await export_to_excel(data=all_questions, headings=[f"{kitob_nomi['table_name']}", "A | CORRECT", "B", "C", "D"],
                          filepath=file_path)

    await call.message.answer_document(types.input_file.FSInputFile(file_path))


# @router.message(Command('reklama'), IsBotAdminFilter(ADMINS))
# async def ask_ad_content(message: types.Message, state: FSMContext):
#     await message.answer("Reklama uchun post yuboring")
#     await state.set_state(AdminState.ask_ad_content)
#
#
# @router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
# async def send_ad_to_users(message: types.Message, state: FSMContext):
#     users = await db.select_all_users()
#     count = 0
#     for user in users:
#         user_id = user[-1]
#         try:
#             await message.send_copy(chat_id=user_id)
#             count += 1
#             await asyncio.sleep(0.05)
#         except Exception as error:
#             logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
#     await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
#     await state.clear()


# @router.message(Command('cleandb'), IsBotAdminFilter(ADMINS))
# async def ask_are_you_sure(message: types.Message, state: FSMContext):
#     msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?")
#     await state.update_data(msg_id=msg.message_id)
#     await state.set_state(AdminState.are_you_sure)
#
#
# @router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(ADMINS))
# async def clean_db(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     msg_id = data.get('msg_id')
#     text = str()
#     if call.data == 'yes':
#         await db.delete_users()
#         text = "Baza tozalandi!"
#     elif call.data == 'no':
#         text = "Bekor qilindi."
#     await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
#     await state.clear()


