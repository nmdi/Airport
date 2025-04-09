import cv2
import time

def get_rtsp_frames(rtsp_urls):
    caps = [cv2.VideoCapture(url) for url in rtsp_urls]  # Mở tất cả camera
    timestamp = int(time.time())  # Lấy chung một timestamp
    images = []  # Danh sách lưu frames

    for i, cap in enumerate(caps):
        if not cap.isOpened():
            print(f"Không thể kết nối đến camera {i+1}")
            images.append(None)
            continue

    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"Không thể đọc frame từ camera {i+1}")
            images.append(None)
        else:
            images.append(frame)
            cv2.imshow(f"Camera {i+1}", frame)  # Hiển thị ảnh

    for cap in caps:
        cap.release()  # Đóng tất cả camera

    return {"images": images, "timestamp": timestamp}  # Trả về danh sách frames và timestamp

