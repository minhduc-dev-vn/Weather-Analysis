# src/utils.py
"""
Module tiện ích cho việc validation và xử lý dữ liệu.

Chức năng:
    - Kiểm tra column tồn tại
    - Validate dữ liệu
    - Helper functions

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
from typing import List, Optional


def validate_columns(df: pd.DataFrame, required_columns: List[str], context: str = "") -> bool:
    """
    Kiểm tra xem các cột bắt buộc có tồn tại trong DataFrame không.
    
    Args:
        df: DataFrame cần kiểm tra
        required_columns: Danh sách các cột bắt buộc
        context: Ngữ cảnh để hiển thị message rõ ràng hơn
    
    Returns:
        bool: True nếu tất cả columns tồn tại, False nếu thiếu
    
    Example:
        >>> validate_columns(df, ['Nhiệt Độ', 'Độ Ẩm'], 'vẽ biểu đồ')
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        context_msg = f" ({context})" if context else ""
        print(f"❌ Thiếu các cột{context_msg}: {missing_cols}")
        print(f"   Các cột có sẵn: {df.columns.tolist()}")
        return False
    
    return True


def safe_get_column(df: pd.DataFrame, column_name: str, default=None):
    """
    Lấy cột từ DataFrame một cách an toàn.
    
    Args:
        df: DataFrame
        column_name: Tên cột
        default: Giá trị mặc định nếu cột không tồn tại
    
    Returns:
        Series hoặc giá trị default
    """
    if column_name in df.columns:
        return df[column_name]
    else:
        print(f"⚠️ Cột '{column_name}' không tồn tại, trả về giá trị mặc định")
        return default


# Danh sách các cột chuẩn (tiếng Việt) sau khi cleaned
STANDARD_COLUMNS = {
    'time': 'Thời Gian',
    'temp': 'Nhiệt Độ',
    'feels_like': 'Nhiệt Độ Cảm Nhận',
    'humidity': 'Độ Ẩm',
    'pressure': 'Áp Suất',
    'wind_speed': 'Tốc Gió',
    'wind_deg': 'Hướng Gió',
    'clouds': 'Độ Che Phủ Mây',
    'visibility': 'Tầm Nhìn',
    'description': 'Mô Tả',
    'city_name': 'Thành Phố'
}

# Danh sách cột bắt buộc
REQUIRED_COLUMNS = ['Thời Gian', 'Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió']

# Danh sách cột tùy chọn
OPTIONAL_COLUMNS = ['Nhiệt Độ Cảm Nhận', 'Hướng Gió', 'Độ Che Phủ Mây', 'Tầm Nhìn', 'Mô Tả']


if __name__ == "__main__":
    # Test
    test_df = pd.DataFrame({
        'Thời Gian': [1, 2, 3],
        'Nhiệt Độ': [25, 26, 27]
    })
    
    print(validate_columns(test_df, ['Thời Gian', 'Nhiệt Độ'], 'test'))
    print(validate_columns(test_df, ['Độ Ẩm'], 'test'))
