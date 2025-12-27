# src/statistics.py
"""
Module tính toán thống kê dữ liệu thời tiết.

Chức năng:
    - Tính toán các chỉ số thống kê (trung bình, min, max, độ lệch)
    - Phân tích xu hướng thời tiết
    - Tạo báo cáo thống kê

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
import os
from typing import Dict, Optional, Tuple, Any
from .config import DEFAULT_CITY_VIET, get_processed_data_path


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Tính toán thống kê cho các cột dữ liệu.
    
    Args:
        df: DataFrame chứa dữ liệu thời tiết
        
    Returns:
        Dict chứa thống kê: {cột: {chỉ_số: giá_trị}}
        
    Example:
        >>> stats = calculate_statistics(df)
        >>> print(stats['Nhiệt Độ']['mean'])
        25.5
    """
    
    stats = {}
    
    # Các cột cần tính toán
    numeric_columns = ['Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió']
    
    for col in numeric_columns:
        if col in df.columns:
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
    
    return stats


def analyze_trend(df: pd.DataFrame) -> Dict[str, str]:
    """
    Phân tích xu hướng thời tiết (tăng/giảm).
    
    Args:
        df: DataFrame dữ liệu thời tiết
        
    Returns:
        Dict chứa xu hướng cho các cột
        
    Example:
        >>> trends = analyze_trend(df)
        >>> print(trends['Nhiệt Độ'])
        'Tăng'
    """
    
    trends = {}
    
    numeric_columns = ['Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió']
    
    for col in numeric_columns:
        if col in df.columns and len(df) > 1:
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
    
    return trends


def get_weather_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Tạo tóm tắt thời tiết.
    
    Args:
        df: DataFrame dữ liệu thời tiết
        
    Returns:
        Dict chứa tóm tắt thời tiết
    """
    
    summary = {
        'Thời gian': {
            'Từ': df['Thời Gian'].min(),
            'Đến': df['Thời Gian'].max(),
            'Tổng mốc': len(df)
        },
        'Nhiệt độ': {
            'Trung bình': f"{df['Nhiệt Độ'].mean():.1f}°C",
            'Cao nhất': f"{df['Nhiệt Độ'].max():.1f}°C",
            'Thấp nhất': f"{df['Nhiệt Độ'].min():.1f}°C",
            'Biến động': f"{df['Nhiệt Độ'].max() - df['Nhiệt Độ'].min():.1f}°C"
        },
        'Độ ẩm': {
            'Trung bình': f"{df['Độ Ẩm'].mean():.0f}%",
            'Cao nhất': f"{df['Độ Ẩm'].max()}%",
            'Thấp nhất': f"{df['Độ Ẩm'].min()}%"
        },
        'Tốc gió': {
            'Trung bình': f"{df['Tốc Gió'].mean():.2f} m/s",
            'Cao nhất': f"{df['Tốc Gió'].max():.2f} m/s",
            'Thấp nhất': f"{df['Tốc Gió'].min():.2f} m/s"
        },
        'Thời tiết phổ biến': df['Mô Tả'].value_counts().index[0] if len(df) > 0 else 'Không có dữ liệu'
    }
    
    return summary


def print_full_statistics(city_name_viet: str = DEFAULT_CITY_VIET, df: Optional[pd.DataFrame] = None) -> None:
    """
    In ra báo cáo thống kê đầy đủ.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
        df: DataFrame dữ liệu (nếu None sẽ đọc từ file)
    """
    
    # ===== ĐỌC DỮ LIỆU =====
    if df is None:
        processed_data_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_data_path):
            print(f"❌ LỖI: Không tìm thấy file dữ liệu sạch cho {city_name_viet}")
            return
        
        df = pd.read_csv(processed_data_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
    
    # ===== TIÊU ĐỀ =====
    print("\n" + "="*70)
    print(" "*15 + f"📊 BÁO CÁO THỐNG KÊ THỜI TIẾT - {city_name_viet}")
    print("="*70 + "\n")
    
    # ===== TÓMLẶT =====
    summary = get_weather_summary(df)
    
    print("📅 THÔNG TIN THỜI GIAN:")
    print(f"  • Từ:        {summary['Thời gian']['Từ']}")
    print(f"  • Đến:       {summary['Thời gian']['Đến']}")
    print(f"  • Tổng mốc:  {summary['Thời gian']['Tổng mốc']} mốc\n")
    
    # ===== NHIỆT ĐỘ =====
    print("🌡️ THỐNG KÊ NHIỆT ĐỘ:")
    for key, val in summary['Nhiệt độ'].items():
        print(f"  • {key:15}: {val}")
    print()
    
    # ===== ĐỘ ẨM =====
    print("💧 THỐNG KÊ ĐỘ ẨM:")
    for key, val in summary['Độ ẩm'].items():
        print(f"  • {key:15}: {val}")
    print()
    
    # ===== TỐC GIÓ =====
    print("💨 THỐNG KÊ TỐC GIÓ:")
    for key, val in summary['Tốc gió'].items():
        print(f"  • {key:15}: {val}")
    print()
    
    # ===== THỜI TIẾT PHỔ BIẾN =====
    print("☁️ THỜI TIẾT PHỔ BIẾN:")
    print(f"  • {summary['Thời tiết phổ biến']}\n")
    
    # ===== XU HƯỚNG =====
    print("📈 XU HƯỚNG (So sánh đầu → cuối):")
    trends = analyze_trend(df)
    for key, val in trends.items():
        print(f"  • {key:15}: {val}")
    print()
    
    # ===== THỐNG KÊ CHI TIẾT =====
    print("📋 THỐNG KÊ CHI TIẾT:")
    stats = calculate_statistics(df)
    
    for col, col_stats in stats.items():
        print(f"\n  {col}:")
        print(f"    • Số mốc:      {col_stats['count']}")
        print(f"    • Trung bình:  {col_stats['mean']}")
        print(f"    • Tối thiểu:   {col_stats['min']}")
        print(f"    • Tối đa:      {col_stats['max']}")
        print(f"    • Độ lệch:     {col_stats['std']}")
        print(f"    • Trung vị:    {col_stats['median']}")
        print(f"    • Q1 (25%):    {col_stats['q25']}")
        print(f"    • Q3 (75%):    {col_stats['q75']}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_full_statistics()
