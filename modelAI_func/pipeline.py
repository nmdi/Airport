import cv2
from PIL import Image
from modelAI_func.collide import collide
from modelAI_func.detect import detection
from modelAI_func.number import num
from modelAI_func.V import v

def main(video_path):
    # Bước 1: Xử lý video để lấy ảnh khi người rời khỏi vùng giám sát
    frame_ra = process_video(video_path)
    if frame_ra is None:
        print("Không tìm thấy sự kiện đáng chú ý trong video.")
        return None
    
    # Chuyển frame sang định dạng PIL để xử lý tiếp
    image_pil = Image.fromarray(cv2.cvtColor(frame_ra, cv2.COLOR_BGR2RGB))
    
    # Bước 2: Chạy mô hình phát hiện đối tượng
    result, detected_objects = detection(image_pil)
    print("Kết quả nhận diện đối tượng:", result, detected_objects)
    
    # Nếu kết quả từ detect là OUT, dừng pipeline và trả về None
    if result == "OUT":
        print("Đối tượng không hợp lệ, dừng xử lý.")
        return None
    
    # Bước 3: Xử lý tiếp dựa trên kết quả
    if detected_objects.get("cart", False):
        # Nếu có xe đẩy, nhận diện biển số
        plate_numbers = num(frame_ra)
        print("Biển số nhận diện được:", plate_numbers)
    else:
        # Nếu không có xe đẩy, phân tích thông tin khác
        extracted_texts = v(frame_ra)
        print("Thông tin trích xuất:", extracted_texts)

if __name__ == "__main__":
    video_path = "input_video.mp4"  # Đổi thành đường dẫn video thực tế
    main(video_path)
