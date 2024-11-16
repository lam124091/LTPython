import json
import os

# Đọc màu từ file colors.json
with open('colors.json', 'r') as f:
    COLORS = json.load(f)

# Đường dẫn file dữ liệu
DATA_FILE = 'Cleaned_data_for_model.csv'
DATA_PATH = os.path.join(os.path.dirname(__file__), DATA_FILE)

# Cấu hình giao diện
WINDOW_SIZES = {
    'main': "400x450",
    'data_viewer': "1200x600",
    'data_explorer': "800x600"
}

# Cấu hình hiển thị dữ liệu
ROWS_PER_PAGE = 1000
