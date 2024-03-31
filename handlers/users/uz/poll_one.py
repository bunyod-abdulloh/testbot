from aiogram import Router, F, types

router = Router()


@router.callback_query(F.data == "uz_random_opponent")
async def uz_random_opponent(call: types.CallbackQuery):
    pass
