from aiogram import Router

from filters import ChatPrivateFilter
from filters.is_group import ChatTypeFilter, IsAdmin


def setup_routers() -> Router:
    from .admin import add_book, add_questions, delete_book, download_excel, edit_book, main, users_, sos_admin, results
    from .users import (battle_main, random_second, random_first, with_friend, playing_alone, start, rating_main,
                        sos_users)
    from .errors import error_handler

    router = Router()

    # Users
    router.include_routers(
        start.router, battle_main.router, random_first.router, random_second.router, with_friend.router,
        playing_alone.router, rating_main.router, sos_users.router)

    # Admin
    router.include_routers(
        add_book.router, add_questions.router, delete_book.router, download_excel.router, edit_book.router,
        main.router, users_.router, sos_admin.router, results.router
    )

    # Errors | BOT
    router.include_routers(
        error_handler.router
    )
    return router
