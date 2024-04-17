from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import admin, help
    from handlers.users.uz import start, battle_main, random_first, random_second
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(
        admin.router,
        start.router,
        battle_main.router,
        random_first.router,
        random_second.router,
        help.router,
        error_handler.router
    )
    return router
