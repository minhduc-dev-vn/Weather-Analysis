# src/config.py
import os

# --- 1. CẤU HÌNH API ---
# ⚠️ QUAN TRỌNG: Thay mã API của bạn vào dòng dưới
API_KEY = "b02db493f6dc047df6014e51c62594f9" 

CITY_NAME = "Hanoi"  # Hoặc "Ho Chi Minh City"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# --- 2. CẤU HÌNH ĐƯỜNG DẪN FILE (PATH) ---
# Lấy đường dẫn gốc của dự án để tránh lỗi "File not found"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Định nghĩa nơi lưu file
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "weather_raw.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "weather_clean.csv")
CHART_PATH = os.path.join(BASE_DIR, "assets", "weather_chart.png")