# src/column_names.py
"""
Module định nghĩa tên cột cho DataFrame.

Mục đích:
    - Tránh hardcode tên cột
    - Đảm bảo tính nhất quán
    - Type safety với Enum
    - Dễ dàng refactor

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

from enum import Enum
from typing import Dict


class RawColumns(str, Enum):
    """
    Tên cột trong raw data (dữ liệu thô từ API).
    Sử dụng tiếng Anh theo chuẩn API OpenWeatherMap.
    """
    
    DT_TXT = 'dt_txt'                # Thời gian dự báo
    TEMP = 'temp'                    # Nhiệt độ
    FEELS_LIKE = 'feels_like'        # Nhiệt độ cảm nhận
    HUMIDITY = 'humidity'            # Độ ẩm
    PRESSURE = 'pressure'            # Áp suất
    WIND_SPEED = 'wind_speed'        # Tốc gió
    WIND_DEG = 'wind_deg'            # Hướng gió
    CLOUDS = 'clouds'                # Độ che phủ mây
    VISIBILITY = 'visibility'        # Tầm nhìn
    DESCRIPTION = 'description'      # Mô tả thời tiết
    CITY_NAME = 'city_name'          # Tên thành phố


class CleanColumns(str, Enum):
    """
    Tên cột trong processed data (dữ liệu đã xử lý).
    Sử dụng tiếng Việt để dễ đọc và hiển thị.
    """
    
    THOI_GIAN = 'Thời Gian'              # DateTime
    NHIET_DO = 'Nhiệt Độ'                # Nhiệt độ (°C)
    NHIET_DO_CAM_NHAN = 'Nhiệt Độ Cảm Nhận'  # Nhiệt độ cảm nhận (°C)
    DO_AM = 'Độ Ẩm'                      # Độ ẩm (%)
    AP_SUAT = 'Áp Suất'                  # Áp suất (hPa)
    TOC_GIO = 'Tốc Gió'                  # Tốc gió (m/s)
    HUONG_GIO = 'Hướng Gió'              # Hướng gió (độ)
    MAY = 'Mây'                          # Độ che phủ mây (%)
    TAM_NHIN = 'Tầm Nhìn'                # Tầm nhìn (km)
    MO_TA = 'Mô Tả'                      # Mô tả thời tiết
    THANH_PHO = 'Thành Phố'              # Tên thành phố


# Mapping từ raw columns sang clean columns
RAW_TO_CLEAN_MAPPING: Dict[str, str] = {
    RawColumns.DT_TXT.value: CleanColumns.THOI_GIAN.value,
    RawColumns.TEMP.value: CleanColumns.NHIET_DO.value,
    RawColumns.FEELS_LIKE.value: CleanColumns.NHIET_DO_CAM_NHAN.value,
    RawColumns.HUMIDITY.value: CleanColumns.DO_AM.value,
    RawColumns.PRESSURE.value: CleanColumns.AP_SUAT.value,
    RawColumns.WIND_SPEED.value: CleanColumns.TOC_GIO.value,
    RawColumns.WIND_DEG.value: CleanColumns.HUONG_GIO.value,
    RawColumns.CLOUDS.value: CleanColumns.MAY.value,
    RawColumns.VISIBILITY.value: CleanColumns.TAM_NHIN.value,
    RawColumns.DESCRIPTION.value: CleanColumns.MO_TA.value,
    RawColumns.CITY_NAME.value: CleanColumns.THANH_PHO.value,
}

# Mapping ngược lại (clean -> raw)
CLEAN_TO_RAW_MAPPING: Dict[str, str] = {
    v: k for k, v in RAW_TO_CLEAN_MAPPING.items()
}


def get_clean_column_name(raw_column: str) -> str:
    """
    Chuyển đổi tên cột raw sang tên cột clean.
    
    Args:
        raw_column: Tên cột trong raw data
        
    Returns:
        str: Tên cột tương ứng trong clean data
        
    Example:
        >>> get_clean_column_name('temp')
        'Nhiệt Độ'
    """
    return RAW_TO_CLEAN_MAPPING.get(raw_column, raw_column)


def get_raw_column_name(clean_column: str) -> str:
    """
    Chuyển đổi tên cột clean sang tên cột raw.
    
    Args:
        clean_column: Tên cột trong clean data
        
    Returns:
        str: Tên cột tương ứng trong raw data
        
    Example:
        >>> get_raw_column_name('Nhiệt Độ')
        'temp'
    """
    return CLEAN_TO_RAW_MAPPING.get(clean_column, clean_column)


def rename_to_clean(df_columns: list) -> Dict[str, str]:
    """
    Tạo dictionary để rename columns từ raw sang clean.
    
    Args:
        df_columns: Danh sách tên cột hiện tại trong DataFrame
        
    Returns:
        Dict[str, str]: Dictionary mapping {old_name: new_name}
        
    Example:
        >>> df_columns = ['dt_txt', 'temp', 'humidity']
        >>> rename_to_clean(df_columns)
        {'dt_txt': 'Thời Gian', 'temp': 'Nhiệt Độ', 'humidity': 'Độ Ẩm'}
    """
    return {
        col: get_clean_column_name(col)
        for col in df_columns
        if col in RAW_TO_CLEAN_MAPPING
    }


def rename_to_raw(df_columns: list) -> Dict[str, str]:
    """
    Tạo dictionary để rename columns từ clean sang raw.
    
    Args:
        df_columns: Danh sách tên cột hiện tại trong DataFrame
        
    Returns:
        Dict[str, str]: Dictionary mapping {old_name: new_name}
        
    Example:
        >>> df_columns = ['Thời Gian', 'Nhiệt Độ', 'Độ Ẩm']
        >>> rename_to_raw(df_columns)
        {'Thời Gian': 'dt_txt', 'Nhiệt Độ': 'temp', 'Độ Ẩm': 'humidity'}
    """
    return {
        col: get_raw_column_name(col)
        for col in df_columns
        if col in CLEAN_TO_RAW_MAPPING
    }


# Các cột bắt buộc phải có trong clean data
REQUIRED_CLEAN_COLUMNS = [
    CleanColumns.THOI_GIAN,
    CleanColumns.NHIET_DO,
    CleanColumns.DO_AM,
]

# Các cột numeric để tính toán thống kê
NUMERIC_CLEAN_COLUMNS = [
    CleanColumns.NHIET_DO,
    CleanColumns.NHIET_DO_CAM_NHAN,
    CleanColumns.DO_AM,
    CleanColumns.AP_SUAT,
    CleanColumns.TOC_GIO,
]
