# src/statistics.py
"""
Module tính toán thống kê dữ liệu thời tiết.

Chức năng:
    - Tính toán các chỉ số thống kê (trung bình, min, max, độ lệch)
    - Phân tích xu hướng thời tiết
    - Tạo báo cáo thống kê

Author: Weather Forecast Pro Team
Date: 2025-12-27 (Refactored for code quality)
"""

import pandas as pd
import os
from typing import Dict, Optional, Any

from .config import DEFAULT_CITY_VIET, get_processed_data_path
from .column_names import CleanColumns, NUMERIC_CLEAN_COLUMNS
from .exceptions import FileOperationError, EmptyDataFrameError, MissingColumnError
from .logger import get_logger, log_success, log_error, log_warning


# Logger cho module này
logger = get_logger(__name__)


def _validate_dataframe_not_empty(df: pd.DataFrame) -> None:
    """
    Validate DataFrame không rỗng.
    
    Args:
        df: DataFrame cần kiểm tra
        
    Raises:
        EmptyDataFrameError: Nếu DataFrame rỗng
    """
    if df is None or len(df) == 0:
        error_msg = "DataFrame rỗng - không thể tính toán thống kê"
        log_error(error_msg, logger)
        raise EmptyDataFrameError(error_msg)


def _validate_columns_exist(df: pd.DataFrame, columns: list) -> None:
    """
    Validate các cột cần thiết tồn tại.
    
    Args:
        df: DataFrame cần kiểm tra
        columns: List các tên cột cần kiểm tra
        
    Raises:
        MissingColumnError: Nếu thiếu cột bắt buộc
    """
    for col in columns:
        if col not in df.columns:
            log_error(f"Thiếu cột bắt buộc: {col}", logger)
            raise MissingColumnError(col, df.columns.tolist())


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Tính toán thống kê cho các cột dữ liệu.
    
    Args:
        df: DataFrame chứa dữ liệu thời tiết
        
    Returns:
        Dict chứa thống kê: {cột: {chỉ_số: giá_trị}}
        
    Raises:
        EmptyDataFrameError: Nếu DataFrame rỗng
        
    Example:
        >>> stats = calculate_statistics(df)
        >>> print(stats['Nhiệt Độ']['mean'])
        25.5
    """
    
    _validate_dataframe_not_empty(df)
    
    stats = {}
    
    # Các cột numeric để tính toán
    numeric_columns = [col.value for col in NUMERIC_CLEAN_COLUMNS if col.value in df.columns]
    
    for col in numeric_columns:
        try:
            stats[col] = {
                'count': int(df[col].count()),
                'mean': round(df[col].mean(), 2),      # Trung bình
                'min': round(df[col].min(), 2),        # Tối thiểu
                'max': round(df[col].max(), 2),        # Tối đa
                'std': round(df[col].std(), 2),        # Độ lệch chuẩn
                'median': round(df[col].median(), 2),  # Trung vị
                'q25': round(df[col].quantile(0.25), 2),  # Phần tư thứ 1
                'q75': round(df[col].quantile(0.75), 2),  # Phần tư thứ 3
            }
        except Exception as e:
            log_warning(f"Không thể tính toán thống kê cho cột {col}: {e}", logger)
            continue
    
    return stats


def analyze_trend(df: pd.DataFrame) -> Dict[str, str]:
    """
    Phân tích xu hướng thời tiết (tăng/giảm).
    
    Args:
        df: DataFrame dữ liệu thời tiết
        
    Returns:
        Dict chứa xu hướng cho các cột
        
    Raises:
        EmptyDataFrameError: Nếu DataFrame rỗng
        
    Example:
        >>> trends = analyze_trend(df)
        >>> print(trends['Nhiệt Độ'])
        'Tăng'
    """
    
    _validate_dataframe_not_empty(df)
    
    if len(df) < 2:
        log_warning("Cần ít nhất 2 dòng dữ liệu để phân tích xu hướng", logger)
        return {}
    
    trends = {}
    
    numeric_columns = [col.value for col in NUMERIC_CLEAN_COLUMNS if col.value in df.columns]
    
    for col in numeric_columns:
        try:
            first_val = df[col].iloc[0]
            last_val = df[col].iloc[-1]
            
            if last_val > first_val:
                change_pct = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
                trends[col] = f"📈 Tăng ({change_pct:.1f}%)"
            elif last_val < first_val:
                change_pct = ((first_val - last_val) / first_val * 100) if first_val != 0 else 0
                trends[col] = f"📉 Giảm ({change_pct:.1f}%)"
            else:
                trends[col] = "➡️ Ổn định"
        except Exception as e:
            log_warning(f"Không thể phân tích xu hướng cho cột {col}: {e}", logger)
            continue
    
    return trends


def get_weather_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Tạo tóm tắt thời tiết.
    
    Args:
        df: DataFrame dữ liệu thời tiết
        
    Returns:
        Dict chứa tóm tắt thời tiết
        
    Raises:
        EmptyDataFrameError: Nếu DataFrame rỗng
        MissingColumnError: Nếu thiếu cột bắt buộc
    """
    
    _validate_dataframe_not_empty(df)
    _validate_columns_exist(df, [
        CleanColumns.THOI_GIAN.value,
        CleanColumns.NHIET_DO.value,
        CleanColumns.DO_AM.value,
        CleanColumns.TOC_GIO.value
    ])
    
    summary = {
        'Thời gian': {
            'Từ': df[CleanColumns.THOI_GIAN.value].min(),
            'Đến': df[CleanColumns.THOI_GIAN.value].max(),
            'Tổng mốc': len(df)
        },
        'Nhiệt độ': {
            'Trung bình': f"{df[CleanColumns.NHIET_DO.value].mean():.1f}°C",
            'Cao nhất': f"{df[CleanColumns.NHIET_DO.value].max():.1f}°C",
            'Thấp nhất': f"{df[CleanColumns.NHIET_DO.value].min():.1f}°C",
            'Biến động': f"{df[CleanColumns.NHIET_DO.value].max() - df[CleanColumns.NHIET_DO.value].min():.1f}°C"
        },
        'Độ ẩm': {
            'Trung bình': f"{df[CleanColumns.DO_AM.value].mean():.0f}%",
            'Cao nhất': f"{df[CleanColumns.DO_AM.value].max()}%",
            'Thấp nhất': f"{df[CleanColumns.DO_AM.value].min()}%"
        },
        'Tốc gió': {
            'Trung bình': f"{df[CleanColumns.TOC_GIO.value].mean():.2f} m/s",
            'Cao nhất': f"{df[CleanColumns.TOC_GIO.value].max():.2f} m/s",
            'Thấp nhất': f"{df[CleanColumns.TOC_GIO.value].min():.2f} m/s"
        }
    }
    
    # Thêm thời tiết phổ biến nếu có cột Mô Tả
    if CleanColumns.MO_TA.value in df.columns:
        summary['Thời tiết phổ biến'] = df[CleanColumns.MO_TA.value].value_counts().index[0] if len(df) > 0 else 'Không có dữ liệu'
    
    return summary


def print_full_statistics(city_name_viet: str = DEFAULT_CITY_VIET, df: Optional[pd.DataFrame] = None) -> None:
    """
    In ra báo cáo thống kê đầy đủ.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
        df: DataFrame dữ liệu (nếu None sẽ đọc từ file)
        
    Raises:
        FileOperationError: Nếu không tìm thấy file dữ liệu
    """
    
    # Đọc dữ liệu nếu chưa có
    if df is None:
        processed_data_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_data_path):
            error_msg = f"Không tìm thấy file dữ liệu sạch cho {city_name_viet}"
            log_error(error_msg, logger)
            raise FileOperationError(error_msg, processed_data_path)
        
        df = pd.read_csv(processed_data_path)
        df[CleanColumns.THOI_GIAN.value] = pd.to_datetime(df[CleanColumns.THOI_GIAN.value])
    
    # Validate
    _validate_dataframe_not_empty(df)
    
    # Tiêu đề
    logger.info("\n" + "="*70)
    logger.info(" "*15 + f"📊 BÁO CÁO THỐNG KÊ THỜI TIẾT - {city_name_viet}")
    logger.info("="*70 + "\n")
    
    # Tóm tắt
    summary = get_weather_summary(df)
    
    logger.info("📅 THÔNG TIN THỜI GIAN:")
    logger.info(f"  • Từ:        {summary['Thời gian']['Từ']}")
    logger.info(f"  • Đến:       {summary['Thời gian']['Đến']}")
    logger.info(f"  • Tổng mốc:  {summary['Thời gian']['Tổng mốc']} mốc\n")
    
    logger.info("🌡️ THỐNG KÊ NHIỆT ĐỘ:")
    for key, val in summary['Nhiệt độ'].items():
        logger.info(f"  • {key:15}: {val}")
    logger.info("")
    
    logger.info("💧 THỐNG KÊ ĐỘ ẨM:")
    for key, val in summary['Độ ẩm'].items():
        logger.info(f"  • {key:15}: {val}")
    logger.info("")
    
    logger.info("💨 THỐNG KÊ TỐC GIÓ:")
    for key, val in summary['Tốc gió'].items():
        logger.info(f"  • {key:15}: {val}")
    logger.info("")
    
    if 'Thời tiết phổ biến' in summary:
        logger.info("☁️ THỜI TIẾT PHỔ BIẾN:")
        logger.info(f"  • {summary['Thời tiết phổ biến']}\n")
    
    # Xu hướng
    logger.info("📈 XU HƯỚNG (So sánh đầu → cuối):")
    trends = analyze_trend(df)
    for key, val in trends.items():
        logger.info(f"  • {key:15}: {val}")
    logger.info("")
    
    # Thống kê chi tiết
    logger.info("📋 THỐNG KÊ CHI TIẾT:")
    stats = calculate_statistics(df)
    
    for col, col_stats in stats.items():
        logger.info(f"\n  {col}:")
        logger.info(f"    • Số mốc:      {col_stats['count']}")
        logger.info(f"    • Trung bình:  {col_stats['mean']}")
        logger.info(f"    • Tối thiểu:   {col_stats['min']}")
        logger.info(f"    • Tối đa:      {col_stats['max']}")
        logger.info(f"    • Độ lệch:     {col_stats['std']}")
        logger.info(f"    • Trung vị:    {col_stats['median']}")
        logger.info(f"    • Q1 (25%):    {col_stats['q25']}")
        logger.info(f"    • Q3 (75%):    {col_stats['q75']}")
    
    logger.info("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_full_statistics()
