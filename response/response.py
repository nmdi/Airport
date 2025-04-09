import time
def ErrorCollide(ts: float):
    return {
        "ts": ts,  # Timestamp là float, đảm bảo kiểu dữ liệu hợp lệ
        "border": "None",  # Chuyển numpy.int32 → int
        "cart_type": -1,  # Chuyển numpy.int32 → int
        "cart_num": "NaN"  # Đảm bảo cart_num là chuỗi
    }
def ErrorDetection(ts: float):
    return {
        "ts": ts,  # Timestamp là float, đảm bảo kiểu dữ liệu hợp lệ
        "border": "None",  # Chuyển numpy.int32 → int
        "cart_type": 0,  # Chuyển numpy.int32 → int
        "cart_num": "NaN"  # Đảm bảo cart_num là chuỗi
    }
def ErrorStatus(ts:float, border: int, cart_type: int, cart_num: str):
    return {
        "ts": ts,  # Timestamp là float, đảm bảo kiểu dữ liệu hợp lệ
        "border": int(border),  # Chuyển numpy.int32 → int
        "cart_type": cart_type,  # Chuyển numpy.int32 → int
        "cart_num": cart_num  # Đảm bảo cart_num là chuỗi
    }