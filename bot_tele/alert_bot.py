import os
import asyncio
from db import get_all_subscribers
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7086847542:AAE_HZ2xY-tPbW4m5-rhgG-UXOSGCULlLd4")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def gui_canh_bao(thong_bao: str):
    subscribers = get_all_subscribers()
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=thong_bao)
        except Exception as e:
            print(f"Lỗi gửi tin nhắn tới {chat_id}: {e}")
