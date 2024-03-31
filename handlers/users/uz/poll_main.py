from aiogram import Router, F, types

from handlers.users.uz.start import uz_start_buttons
from keyboards.inline.buttons import battle_ibuttons
from loader import bot

router = Router()

uz_battle_buttons = battle_ibuttons(
    random_opponent="Tasodifiy raqib bilan", opponent_callback="uz_random_opponent",
    rival_offer="Raqib taklif qilish", offer_callback="uz_offer",
    playing_alone="Yakka o'yin", alone_callback="uz_alone",
    back="Ortga", back_callback="uz_back"
)


@router.message(F.text == "⚔️ Bellashuv")
async def uz_battle_main(message: types.Message):
    await message.answer(
        text="Bellashuv turini tanlang", reply_markup=uz_battle_buttons
    )


@router.callback_query(F.data == "uz_back")
async def uz_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )


@router.message(F.text == "poll")
async def send_poll(message: types.Message):
    question = "What's your favorite color?"
    options = ["Red", "Blue", "Green", "Yellow"]
    letters = ["A", "B", "C", "D"]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="A", callback_data=options[0]
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="B", callback_data=options[1]
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="C", callback_data=options[2]
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="D", callback_data=options[3]
                )
            ]
        ]
    )
    question_ = str()
    for letter, option in zip(letters, options):
        question_ += f"{letter}) {option}\n"

    # for letter, option in zip(letters[2:], options[2:]):
    #     if letters[2]:
    #         question_ += f"\n{letter}) {option} "
    #     else:
    #         question_ += f"{letter}) {option}"

    await message.answer(
        text=f"{question}\n\n{question_}", reply_markup=keyboard
    )
    # await bot.send_poll(
    #     chat_id=message.from_user.id,
    #     question=question,
    #     options=options,
    #     type='quiz',
    #     close_date=5,
    #     explanation="Bu explanation",
    #     correct_option_id=0
    # )
    # await message.answer("Poll sent successfully! Now wait for user responses.")


@router.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    # Process the poll answer here
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    option_ids = poll_answer.option_ids
    await bot.send_message(chat_id=user_id, text=f"Thanks for voting in the poll (ID: {poll_id})!")
