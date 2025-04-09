from fastapi import FastAPI, HTTPException
import asyncio
from bot_tele.alert_bot import gui_canh_bao
from rtps.RTPS_Streams import get_rtsp_frames
from modelAI_func.detect import detection
from modelAI_func.collide import collide
from modelAI_func.number import num
from modelAI_func.pipeline import process_video
import numpy as np
from response.response import ErrorCollide,ErrorStatus,ErrorDetection

# Danh sách 5 URL RTSP của các camera
rtsp_urls = [
    "rtsp://10.0.10.120:554/profile1",
]

app = FastAPI()

# 🟢 Hàm xử lý AI border model
def func_border(obj):
    """
    Hàm chạy AI border model
    """
    return np.random.choice([0, 1])  # Giả lập kết quả AI border

# 🟢 API Cargo gọi để lấy dữ liệu từ camera và xử lý AI
@app.get("/process_cargo/")
async def process_cargo():
    try:
        # 🔹 Lấy dữ liệu từ camera
        obj = get_rtsp_frames(rtsp_urls)
        status = collide(obj['images'][0])
        if status == 1:
            cart_type = detection(obj)
            if cart_type == "IN":
                cart_num = num(obj)
                border_status = func_border(obj)
                if border_status == 0:
                    alert_msg = f"⚠️ CẢNH BÁO: Xe không chạm vạch!\n📅 Timestamp: {obj['timestamp']}\n🚗 Loại xe: {cart_type}\n🔢 Biển số: {cart_num}"
                    asyncio.run(gui_canh_bao(alert_msg))
                return ErrorStatus(obj['timestamp'], border_status, cart_type, cart_num)
            return ErrorDetection(obj['timestamp'])
        return ErrorCollide(obj['timestamp'])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
