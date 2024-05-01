from aiogram import Router, types, F

router = Router()


@router.message(F.text == "📊 Reyting")
async def router_main(message: types.Message):
    pass
