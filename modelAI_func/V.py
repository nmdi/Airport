import cv2
import easyocr
import numpy as np
import matplotlib.pyplot as plt

def v(image_path):
    # Khởi tạo EasyOCR reader
    reader = easyocr.Reader(['en', 'vi'])
    
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        print("Không tìm thấy ảnh! Kiểm tra lại đường dẫn.")
        return None
    
    # Chuyển ảnh từ BGR sang RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Tọa độ bounding box
    x, y, w, h = 420, 385, 180, 110
    
    # Vẽ bounding box
    cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Hiển thị ảnh có bounding box
    plt.figure(figsize=(6, 6))
    plt.imshow(image_rgb)
    plt.axis("off")
    plt.title("Image with Bounding Box")
    plt.show()
    
    # Cắt ảnh
    cropped_image = image[y:y+h, x:x+w]
    cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    
    # Hiển thị ảnh đã cắt
    plt.figure(figsize=(4, 4))
    plt.imshow(cropped_image_rgb)
    plt.axis("off")
    plt.title("Cropped Image")
    plt.show()
    
    # Chuyển ảnh sang HSV và tách màu vàng
    hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_extracted = cv2.bitwise_and(cropped_image, cropped_image, mask=mask)
    
    # Hiển thị ảnh đã tách màu vàng
    plt.figure(figsize=(4, 4))
    plt.imshow(cv2.cvtColor(yellow_extracted, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title("Chỉ giữ lại màu vàng")
    plt.show()
    
    # Nhận diện chữ bằng EasyOCR
    results = reader.readtext(mask)
    
    # Trích xuất văn bản nhận diện được
    detected_texts = [text for (_, text, _) in results]
    print("📌 Văn bản nhận diện được:")
    for text in detected_texts:
        print(f"🔹 {text}")
    
    return detected_texts
