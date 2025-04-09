import cv2
import easyocr
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load mô hình YOLO
model = YOLO("number.pt")

# Khởi tạo EasyOCR
reader = easyocr.Reader(['en'])

import cv2
import numpy as np

def preprocess_plate(plate_img):   
    # Chuyển ảnh sang xám
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # Tăng tương phản nhẹ để giữ nét chữ L
    brightened = cv2.convertScaleAbs(gray, alpha=1.2, beta=7)  

    # Làm sắc nét nhưng không làm méo chữ
    sharpened = cv2.GaussianBlur(brightened, (3, 3), 0)
    sharpened = cv2.addWeighted(brightened, 1.3, sharpened, -0.3, 0)  # Tăng độ sắc nét nhẹ hơn một chút

    # Thêm bước giảm nhiễu nhẹ để giữ đường nét chữ
    denoised = cv2.fastNlMeansDenoising(sharpened, h=10, templateWindowSize=7, searchWindowSize=21)

    return denoised

def num(obj):
    """
    Nhận dạng biển số từ ảnh đầu vào.
    obj: Đường dẫn ảnh hoặc numpy array của ảnh.
    Trả về: Chuỗi biển số nhận diện được.
    """
    # Đọc ảnh
    if isinstance(obj, str):
        img = cv2.imread(obj)
    else:
        img = obj

    if img is None:
        return "Không thể đọc ảnh."

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Dự đoán với YOLO
    result = model(img)

    plate_texts = []

    # Lấy bounding box của biển số và nhận diện
    for r in result:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Cắt vùng biển số
            plate_img = img[y1:y2, x1:x2]
            processed_plate = preprocess_plate(plate_img)

            # Nhận diện biển số với OCR
            plate_number = reader.readtext(processed_plate, detail=0)
            plate_texts.append(" ".join(plate_number))

            # Vẽ bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Hiển thị ảnh biển số đã crop
            plt.figure(figsize=(4, 2))
            plt.imshow(processed_plate, cmap="gray")
            plt.axis("off")
            plt.title(f"Biển số: {plate_number}")
            plt.show()

    # Hiển thị ảnh gốc với bounding box
    # plt.figure(figsize=(8, 6))
    # plt.imshow(img)
    # plt.axis("off")
    # plt.title("Kết quả nhận diện biển số")
    # plt.show()

    return plate_texts if plate_texts else "Không tìm thấy biển số."
