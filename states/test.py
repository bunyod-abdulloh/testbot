from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    add_data_to_db = State()
    add_book_to_db = State()
    are_you_sure = State()
    ask_ad_content = State()
