import os
import re
from PIL import Image

def resize_assets():
    source_file = "icon.png"
    
    if not os.path.exists(source_file):
        print(f"Lỗi: Không tìm thấy file gốc '{source_file}'")
        return

    # Danh sách không được chạm vào
    exclude_files = ['logo.png', 'logo.svg', 'icon.png', 'icon.svg']
    
    # Quy tắc kích thước cho các file không ghi số trong tên
    special_cases = {
        "apple-touch-icon.png": (180, 180),
        "apple-touch-icon-precomposed.png": (180, 180),
        "mstile-150x150.png": (150, 150), # Đôi khi regex không bắt được nếu viết dính
    }

    pattern = re.compile(r'(\d+)x(\d+)')

    print(f"--- Bắt đầu xử lý bộ icon cho Khôi ---")

    for filename in os.listdir('.'):
        # Chỉ làm việc với png và ico, bỏ qua file loại trừ
        if filename in exclude_files or not filename.lower().endswith(('.png', '.ico')):
            continue

        try:
            with Image.open(source_file) as img:
                target_size = None

                # 1. Kiểm tra các file đặc biệt (Apple/MS)
                if filename in special_cases:
                    target_size = special_cases[filename]
                
                # 2. Kiểm tra nếu có kích thước trong tên (ví dụ: 144x144)
                else:
                    match = pattern.search(filename)
                    if match:
                        target_size = (int(match.group(1)), int(match.group(2)))

                # Tiến hành Resize và Lưu
                if target_size:
                    # Xử lý riêng cho ICO
                    if filename.lower().endswith('.ico'):
                        # File .ico nên chứa nhiều size để tương thích tốt
                        img.save(filename, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
                        print(f"√ Đã đóng gói ICO: {filename}")
                    else:
                        # Resize PNG chất lượng cao
                        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                        resized_img.save(filename)
                        print(f"√ Đã resize PNG: {filename} -> {target_size[0]}x{target_size[1]}")
                else:
                    print(f"! Bỏ qua (không xác định được size): {filename}")
        
        except Exception as e:
            print(f"X Lỗi file {filename}: {e}")

    print("--- Hoàn tất! Tất cả icon đã đồng bộ với icon.png ---")

if __name__ == "__main__":
    resize_assets()