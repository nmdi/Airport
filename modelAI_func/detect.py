import torch
import cv2
import numpy as np
import os
from ultralytics import YOLOv10
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image

def detection(obj):
    """Nhận diện xe đẩy và bánh xe từ ảnh đầu vào, kiểm tra xem xe có nằm trong vùng quy định không."""
    
    # 🛠️ Thiết lập mô hình YOLO
    model_path = '/content/data/model/train/weights/best.pt'
    model = YOLOv10(model_path)
    
    # 🛠️ Thiết lập mô hình SAM2
    sam2_checkpoint = "/checkpoints/sam2.1_hiera_large.pt"
    model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)
    predictor = SAM2ImagePredictor(sam2_model)
    
    # 🖼️ Chuyển đổi ảnh đầu vào
    image_np = np.array(obj.convert("RGB"))
    
    # 📂 Lưu ảnh tạm để YOLO xử lý
    temp_image_path = "/content/temp_image.jpg"
    obj.save(temp_image_path)
    
    # 🎯 Dự đoán bằng YOLO
    results = model.track(source=temp_image_path, save=True, conf=0.5, persist=True)
    
    # 📌 Lấy danh sách đối tượng
    class_ids = results[0].boxes.cls.int().cpu().tolist()
    boxes = results[0].boxes.xyxy.float().cpu().tolist()

    # 🚗 Kiểm tra xem có xe đẩy không (Giả sử class_id == 2 là xe đẩy)
    has_cart = 2 in class_ids
    cart_boxes = [boxes[i] for i in range(len(class_ids)) if class_ids[i] == 2]

    # 🛞 Lấy vị trí bánh xe (Giả sử class_id == 1 là bánh xe)
    wheel_boxes = [boxes[i] for i in range(len(class_ids)) if class_ids[i] == 1]
    wheel_points = [(box[0] + box[2]) / 2 for box in wheel_boxes]

    # 🛑 Nếu không có xe đẩy hoặc quá ít bánh xe, trả về OUT
    if not has_cart or len(wheel_boxes) < 2:
        return "OUT", {"cart": has_cart, "wheels": len(wheel_boxes)}

    # 🎯 Dự đoán phân vùng xe đẩy bằng SAM2
    predictor.set_image(image_np)
    input_point = np.array([[150, 410]])  # 🎯 Điểm cố định để xác định vùng xe đẩy
    input_label = np.array([1])

    masks, scores, _ = predictor.predict(point_coords=input_point, point_labels=input_label, multimask_output=False)
    
    # 🔍 Xác định vùng biên xe đẩy
    mask_image = masks.astype(np.uint8).reshape(masks.shape[-2:])
    left_most, right_most = mask_image.shape[1] - 1, 0
    for i in range(mask_image.shape[0]):
        for j in range(mask_image.shape[1]):
            if mask_image[i][j] == 1:
                left_most = min(left_most, j)
                right_most = max(right_most, j)
    
    # ✅ Kiểm tra vị trí bánh xe
    is_in = all(left_most <= wheel <= right_most for wheel in wheel_points)

    # 📌 Kết quả trả về
    text = "IN" if is_in else "OUT"
    detected_objects = {"cart": has_cart, "wheels": len(wheel_boxes)}
    
    return text, detected_objects
