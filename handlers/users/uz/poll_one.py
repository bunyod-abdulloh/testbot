import asyncio

from aiogram import Router, F, types

from data.config import GROUP_ID
from keyboards.inline.buttons import to_offer_ibuttons, OfferCallback
from loader import db, bot

router = Router()

