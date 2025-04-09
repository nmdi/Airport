import asyncio
from bot_tele.alert_bot import gui_canh_bao

if __name__ == "__main__":
    message = "🚨Cảnh báo: Phát hiện xe ngoài vạch!"
    asyncio.run(gui_canh_bao(message))
