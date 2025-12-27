# src/constants.py
"""
Module chứa tất cả các hằng số và giá trị cấu hình.

Mục đích:
    - Loại bỏ magic numbers
    - Tập trung cấu hình vào một nơi
    - Dễ bảo trì và thay đổi

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

from typing import Tuple

# ==================== API CONFIGURATION ====================
API_TIMEOUT_SECONDS = 10  # Thời gian chờ API response (giây)
API_RETRY_ATTEMPTS = 3    # Số lần thử lại khi gọi API thất bại
API_RETRY_DELAY = 2       # Thời gian chờ giữa các lần retry (giây)

# ==================== DATA VALIDATION THRESHOLDS ====================
# Nhiệt độ
MIN_VALID_TEMPERATURE = -100.0  # Độ C (nhiệt độ thấp nhất vật lý)
MAX_VALID_TEMPERATURE = 70.0    # Độ C (nhiệt độ cao nhất vật lý)

# Độ ẩm
MIN_VALID_HUMIDITY = 0.0    # Phần trăm
MAX_VALID_HUMIDITY = 100.0  # Phần trăm

# Tốc gió
MIN_VALID_WIND_SPEED = 0.0   # m/s
MAX_VALID_WIND_SPEED = 150.0 # m/s (max cho bão cấp 5)

# Áp suất
MIN_VALID_PRESSURE = 800.0   # hPa
MAX_VALID_PRESSURE = 1100.0  # hPa

# ==================== CHART CONFIGURATION ====================
# Kích thước biểu đồ (tăng size cho dễ nhìn hơn)
DEFAULT_FIGSIZE: Tuple[int, int] = (14, 7)  # Tăng từ (12, 6)
LARGE_FIGSIZE: Tuple[int, int] = (16, 9)   # Tăng từ (14, 8)
SMALL_FIGSIZE: Tuple[int, int] = (12, 6)   # Tăng từ (10, 5)
MULTI_CHART_FIGSIZE: Tuple[int, int] = (16, 10)

# DPI (dots per inch) - tăng để sắc nét hơn
DEFAULT_DPI = 120  # Tăng từ 100
HIGH_DPI = 200     # Tăng từ 150

# Histogram
HISTOGRAM_BINS = 10
HISTOGRAM_ALPHA = 0.7

# Màu sắc biểu đồ - vibrant và modern
COLOR_TEMPERATURE = '#FF6B6B'      # Đỏ coral cho nhiệt độ
COLOR_TEMPERATURE_GRADIENT = '#FF8E53'  # Cam gradient
COLOR_HUMIDITY = '#4ECDC4'         # Xanh turquoise cho độ ẩm  
COLOR_HUMIDITY_GRADIENT = '#45B7D1'     # Xanh dương gradient
COLOR_WIND = '#95E1D3'             # Xanh mint cho gió
COLOR_PRESSURE = '#FFA07A'         # Cam salmon cho áp suất
COLOR_GRID = '#E0E0E0'             # Grid xám nhạt
COLOR_GAUSSIAN = '#2ECC71'         # Xanh lá sáng

# Độ trong suốt
ALPHA_FILL = 0.3
ALPHA_LINE = 0.8
ALPHA_HISTOGRAM = 0.7

# Line width - tăng để rõ hơn
LINE_WIDTH_DEFAULT = 2.5  # Tăng từ 2
LINE_WIDTH_THICK = 3.5    # Tăng từ 3  
LINE_WIDTH_THIN = 2.0     # Tăng từ 1.5

# Grid
GRID_ALPHA = 0.3
GRID_LINESTYLE = '--'

# ==================== FONT CONFIGURATION ====================
FONT_FAMILY = 'Arial'
FONT_WEIGHT_NORMAL = 'normal'
FONT_WEIGHT_BOLD = 'bold'

# Font sizes - tăng cho dễ đọc
FONT_SIZE_TITLE = 18      # Tăng từ 16
FONT_SIZE_LABEL = 13      # Tăng từ 12
FONT_SIZE_TICK = 11       # Tăng từ 10
FONT_SIZE_LEGEND = 11     # Tăng từ 10
FONT_SIZE_SMALL = 9       # Tăng từ 8

# ==================== UI CONFIGURATION ====================
# Cửa sổ chính
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_TITLE = "🌤️ Weather Forecast Pro - Dự Báo Thời Tiết v3.0"

# Padding
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 20

# Button dimensions
BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

# Text widget dimensions
TEXT_WIDGET_WIDTH = 80
TEXT_WIDGET_HEIGHT_SMALL = 15
TEXT_WIDGET_HEIGHT_MEDIUM = 20
TEXT_WIDGET_HEIGHT_LARGE = 30

# Frame relief
FRAME_RELIEF = 'groove'
FRAME_BORDER_WIDTH = 2

# ==================== DATA DISPLAY LIMITS ====================
# Số dòng hiển thị mặc định
DEFAULT_DISPLAY_ROWS = 12  # df.head(12)
SAMPLE_DISPLAY_ROWS = 5    # Hiển thị mẫu

# Số mốc thời gian hiển thị trên biểu đồ
MAX_TIME_POINTS_DISPLAY = 12  # 48 giờ (mỗi mốc 3 giờ)

# ==================== FILE PATHS ====================
# Tên file
RAW_DATA_FILENAME_PREFIX = "weather_raw_"
PROCESSED_DATA_FILENAME_PREFIX = "weather_clean_"
CHART_FILENAME_PREFIX = "weather_chart_"

# Extensions
CSV_EXTENSION = ".csv"
PNG_EXTENSION = ".png"
LOG_EXTENSION = ".log"

# ==================== LOGGING CONFIGURATION ====================
LOG_FILENAME = "weather_app.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ==================== DATA PROCESSING ====================
# Missing value handling
MISSING_VALUE_THRESHOLD = 0.5  # Nếu > 50% missing thì loại bỏ cột
INTERPOLATION_METHOD = 'linear'
INTERPOLATION_LIMIT = 3  # Số missing values liên tiếp tối đa để interpolate

# Outlier detection
OUTLIER_STD_THRESHOLD = 3  # Số lần độ lệch chuẩn để coi là outlier

# ==================== EMOJI CONSTANTS ====================
# Cho logging và UI
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_INFO = "💡"
EMOJI_LOADING = "📡"
EMOJI_FILE = "📁"
EMOJI_CHART = "📊"
EMOJI_CITY = "🌆"
EMOJI_TEMPERATURE = "🌡️"
EMOJI_HUMIDITY = "💧"
EMOJI_WIND = "💨"
EMOJI_PRESSURE = "🔽"
EMOJI_CLOUD = "☁️"
EMOJI_STATS = "📈"

# ==================== TIME CONSTANTS ====================
SECONDS_PER_HOUR = 3600
HOURS_PER_DAY = 24
FORECAST_INTERVAL_HOURS = 3  # OpenWeatherMap cung cấp dữ liệu mỗi 3 giờ
