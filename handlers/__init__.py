from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .admin import main, edit_book, add_book, add_questions
    from .users import admin, help
    from .users import battle_main, random_second, random_first, with_friend, playing_alone, start, rating_main
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(
        admin.router,
        start.router, battle_main.router, random_first.router, random_second.router, with_friend.router,
        playing_alone.router, rating_main.router,
        help.router, error_handler.router,
        main.router, edit_book.router, add_book.router, add_questions.router
    )
    return router
