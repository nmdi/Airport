import cv2
import numpy as np
from ultralytics import YOLO

def process_video(video_path):
    """
    Xử lý video, cắt frame khi người vào và rời khỏi vùng tứ giác.
    
    :param video_path: Đường dẫn video đầu vào
    :return: (frame_vao, frame_ra) nếu có, ngược lại trả về None
    """
    cap = cv2.VideoCapture(video_path)
    state_tracker = {"inside": False, "frame_vao": None}
    model = YOLO("yolov8n.pt")  # Load model YOLO một lần
    
    frame_vao, frame_ra = None, None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        polygon_pts = np.array([[80, 500], [380, 552], [424, 474], [150, 420]], np.int32)
        polygon_pts = polygon_pts.reshape((-1, 1, 2))
        
        results = model(frame)
        person_in_zone = False
        
        for result in results:
            for box in result.boxes.data:
                x1, y1, x2, y2, conf, cls = box.tolist()
                if int(cls) == 0:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    person_box = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], np.int32)
                    person_box = person_box.reshape((-1, 1, 2))
                    
                    intersect_result, _ = cv2.intersectConvexConvex(np.array(polygon_pts, dtype=np.float32),
                                                                    np.array(person_box, dtype=np.float32))
                    if intersect_result > 0:  # Nếu có giao nhau
                        person_in_zone = True
                        break
        
        if person_in_zone and not state_tracker["inside"]:
            state_tracker["inside"] = True
            frame_vao = frame.copy()  # Lưu frame lúc vào
        elif not person_in_zone and state_tracker["inside"]:
            state_tracker["inside"] = False
            frame_ra = frame.copy()  # Lưu frame lúc ra
            cap.release()
            return frame_ra  # Trả về cả 2 frame
    
    cap.release()
    return None  # Không có sự kiện nào xảy ra
