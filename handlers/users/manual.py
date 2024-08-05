from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text == "ℹ️ Qo'llanma")
async def router_manual_one(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Botdan foydalanishdan oldin quyidagi <b>ℹ️ Qo'llanma</b>mizni o'qib chiqishingizni so'raymiz:\n\n"
             "https://telegra.ph/Testchi-Robot--Qollanma-05-27"
    )
