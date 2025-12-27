# src/config.py
import os
from typing import Dict, List

# --- 1. CẤU HÌNH API ---
# ⚠️ QUAN TRỌNG: Thay mã API của bạn vào dòng dưới
API_KEY = "b02db493f6dc047df6014e51c62594f9" 

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# --- 2. DANH SÁCH THÀNH PHỐ VIỆT NAM ---
# Tên thành phố theo chuẩn OpenWeatherMap (tiếng Anh)
VIETNAM_CITIES = {
    "Hà Nội": "Hanoi",
    "TP. Hồ Chí Minh": "Ho Chi Minh City",
    "Đà Nẵng": "Da Nang",
    "Cần Thơ": "Can Tho",
    "Nha Trang": "Nha Trang",
    "Huế": "Hue",
    "Vũng Tàu": "Vung Tau",
    "Quy Nhon": "Quy Nhon",
    "Phan Thiet": "Phan Thiet",
    "Đà Lạt": "Da Lat",
    "Hạ Long": "Ha Long"
}

# Thành phố mặc định
DEFAULT_CITY_VIET = "Hà Nội"
DEFAULT_CITY_EN = VIETNAM_CITIES[DEFAULT_CITY_VIET]

# --- 3. CẤU HÌNH ĐƯỜNG DẪN FILE (PATH) ---
# Lấy đường dẫn gốc của dự án để tránh lỗi "File not found"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Định nghĩa nơi lưu file (theo thành phố)
def get_raw_data_path(city_name_viet: str = DEFAULT_CITY_VIET) -> str:
    """Lấy đường dẫn file raw data theo thành phố"""
    city_safe = city_name_viet.replace(" ", "_").replace(".", "")
    return os.path.join(BASE_DIR, "data", "raw", f"weather_raw_{city_safe}.csv")

def get_processed_data_path(city_name_viet: str = DEFAULT_CITY_VIET) -> str:
    """Lấy đường dẫn file processed data theo thành phố"""
    city_safe = city_name_viet.replace(" ", "_").replace(".", "")
    return os.path.join(BASE_DIR, "data", "processed", f"weather_clean_{city_safe}.csv")

def get_chart_path(city_name_viet: str = DEFAULT_CITY_VIET, chart_type: str = "main") -> str:
    """Lấy đường dẫn file biểu đồ theo thành phố và loại"""
    city_safe = city_name_viet.replace(" ", "_").replace(".", "")
    filename = f"weather_chart_{city_safe}_{chart_type}.png"
    return os.path.join(BASE_DIR, "assets", filename)

# Đường dẫn mặc định (tương thích với code cũ)
RAW_DATA_PATH = get_raw_data_path(DEFAULT_CITY_VIET)
PROCESSED_DATA_PATH = get_processed_data_path(DEFAULT_CITY_VIET)
CHART_PATH = get_chart_path(DEFAULT_CITY_VIET, "main")

# Đường dẫn cho biểu đồ so sánh nhiều thành phố
MULTI_CITY_CHART_PATH = os.path.join(BASE_DIR, "assets", "weather_multi_city_comparison.png")