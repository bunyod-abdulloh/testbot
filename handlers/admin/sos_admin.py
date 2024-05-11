from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


@router.message(Command("view"))
async def savollar_view(message: types.Message):
    print("view ishladi")


@router.message(F.text == "olma")
async def savollar_view_(message: types.Message):
    print("olma ishladi")