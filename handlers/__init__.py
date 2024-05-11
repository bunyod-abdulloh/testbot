from aiogram import Router

from filters import ChatPrivateFilter
from filters.is_group import ChatTypeFilter, IsAdmin


def setup_routers() -> Router:
    from .admin import add_book, add_questions, delete_book, download_excel, edit_book, main, users_, sos_admin
    from .users import help
    from .users import (battle_main, random_second, random_first, with_friend, playing_alone, start, rating_main,
                        sos_users)
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    sos_admin.router.message.filter(ChatTypeFilter(["supergroup"]), IsAdmin())
    router.include_routers(
        start.router, battle_main.router, random_first.router, random_second.router, with_friend.router,
        playing_alone.router, rating_main.router, sos_users.router,
        help.router, error_handler.router,
        add_book.router, add_questions.router, delete_book.router, download_excel.router, edit_book.router, main.router,
        users_.router, sos_admin.router
    )
    return router
