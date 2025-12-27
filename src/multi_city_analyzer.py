# src/multi_city_analyzer.py
"""
Module phân tích và so sánh dữ liệu thời tiết giữa nhiều thành phố.

Chức năng:
    - So sánh thống kê giữa các thành phố
    - Tìm thành phố có nhiệt độ cao nhất/thấp nhất
    - Phân tích xu hướng chung
    - Tạo báo cáo so sánh

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
import os
from typing import Dict, List, Optional
from .config import get_processed_data_path, VIETNAM_CITIES
from .statistics import calculate_statistics, analyze_trend
from .logger import get_logger


# Logger for module
logger = get_logger(__name__)


def load_multiple_cities_data(city_list: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Load dữ liệu từ nhiều thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary với key là tên thành phố, value là DataFrame
    """
    
    data_dict = {}
    
    for city in city_list:
        processed_path = get_processed_data_path(city)
        if os.path.exists(processed_path):
            try:
                df = pd.read_csv(processed_path)
                df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
                data_dict[city] = df
                logger.info("Đã load dữ liệu %s: %d mốc", city, len(df))
            except Exception as e:
                logger.warning("Lỗi đọc dữ liệu %s: %s", city, e)
        else:
            logger.warning("Không tìm thấy dữ liệu cho %s", city)
    
    return data_dict


def compare_cities_statistics(city_list: List[str], metric: str = 'Nhiệt Độ') -> pd.DataFrame:
    """
    So sánh thống kê một metric giữa các thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
        metric: Metric cần so sánh (tiếng Việt: 'Nhiệt Độ', 'Độ Ẩm', 'Tốc Gió', 'Áp Suất')
    
    Returns:
        pd.DataFrame: DataFrame chứa thống kê của các thành phố
    """
    
    data_dict = load_multiple_cities_data(city_list)
    
    if len(data_dict) == 0:
        logger.error("Không có dữ liệu để so sánh")
        return pd.DataFrame()
    
    stats_list = []
    
    for city, df in data_dict.items():
        # Validate column exists
        if metric not in df.columns:
            logger.warning("Cột '%s' không tồn tại trong dữ liệu %s", metric, city)
            continue
        
        stats_list.append({
            'Thành Phố': city,
            'Trung Bình': round(df[metric].mean(), 2),
            'Tối Thiểu': round(df[metric].min(), 2),
            'Tối Đa': round(df[metric].max(), 2),
            'Trung Vị': round(df[metric].median(), 2),
            'Độ Lệch Chuẩn': round(df[metric].std(), 2),
            'Số Mốc': len(df)
        })
    
    if len(stats_list) == 0:
        logger.error("Không có dữ liệu hợp lệ để tạo thống kê")
        return pd.DataFrame()
    
    result_df = pd.DataFrame(stats_list)
    result_df = result_df.sort_values('Trung Bình', ascending=False)
    
    return result_df


def find_extreme_cities(city_list: List[str], metric: str = 'Nhiệt Độ') -> Dict[str, str]:
    """
    Tìm thành phố có giá trị cao nhất và thấp nhất cho một metric.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
        metric: Metric cần so sánh
    
    Returns:
        Dict[str, str]: Dictionary chứa thành phố cao nhất và thấp nhất
    """
    
    data_dict = load_multiple_cities_data(city_list)
    
    if len(data_dict) == 0:
        return {}
    
    city_averages = {}
    
    for city, df in data_dict.items():
        if metric in df.columns:
            city_averages[city] = df[metric].mean()
    
    if len(city_averages) == 0:
        return {}
    
    max_city = max(city_averages, key=city_averages.get)
    min_city = min(city_averages, key=city_averages.get)
    
    return {
        'Cao Nhất': f"{max_city} ({city_averages[max_city]:.2f})",
        'Thấp Nhất': f"{min_city} ({city_averages[min_city]:.2f})"
    }


def print_comparison_report(city_list: List[str]) -> None:
    """
    In báo cáo so sánh chi tiết giữa các thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
    """
    
    logger.info("%s", "\n" + "="*80)
    logger.info("%s", " "*25 + "📊 BÁO CÁO SO SÁNH THÀNH PHỐ")
    logger.info("%s", "="*80 + "\n")

    logger.info("📍 Các thành phố được so sánh: %s\n", ', '.join(city_list))
    
    # So sánh từng metric
    metrics = ['Nhiệt Độ', 'Độ Ẩm', 'Tốc Gió']
    
    for metric in metrics:
        logger.info("%s", "\n" + "="*80)
        logger.info("🌡️ SO SÁNH %s", metric.upper())
        logger.info("%s", "="*80)
        
        comparison_df = compare_cities_statistics(city_list, metric)
        if not comparison_df.empty:
            logger.info('\n%s', comparison_df.to_string(index=False))

            extremes = find_extreme_cities(city_list, metric)
            if extremes:
                logger.info('\n🏆 Thành phố %s:', metric)
                logger.info('   • Cao nhất: %s', extremes['Cao Nhất'])
                logger.info('   • Thấp nhất: %s', extremes['Thấp Nhất'])
        else:
            logger.warning("Không có dữ liệu để so sánh %s", metric)
    
    logger.info("%s", "\n" + "="*80 + "\n")


def get_city_ranking(city_list: List[str], metric: str = 'Nhiệt Độ') -> pd.DataFrame:
    """
    Xếp hạng các thành phố theo một metric.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
        metric: Metric để xếp hạng
    
    Returns:
        pd.DataFrame: DataFrame xếp hạng các thành phố
    """
    
    comparison_df = compare_cities_statistics(city_list, metric)
    
    if comparison_df.empty:
        return pd.DataFrame()
    
    comparison_df['Hạng'] = range(1, len(comparison_df) + 1)
    comparison_df = comparison_df[['Hạng', 'Thành Phố', 'Trung Bình', 'Tối Thiểu', 'Tối Đa']]
    
    return comparison_df


if __name__ == "__main__":
    # Chạy thử
    cities = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"]
    print_comparison_report(cities)





