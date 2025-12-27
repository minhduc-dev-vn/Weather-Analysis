# src/data_cleaner.py
"""
Module xử lý và làm sạch dữ liệu thời tiết.

Chức năng:
    - Đọc dữ liệu thô từ CSV
    - Kiểm tra và loại bỏ dữ liệu không hợp lệ
    - Chuẩn hóa định dạng và tên cột
    - Làm tròn số liệu
    - Lưu dữ liệu sạch thành CSV

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
import os
from typing import Optional
from .config import RAW_DATA_PATH, PROCESSED_DATA_PATH


def clean_data() -> Optional[pd.DataFrame]:
    """
    Đọc, xử lý và làm sạch dữ liệu thời tiết.
    
    Quy trình xử lý:
    1. Kiểm tra file dữ liệu thô tồn tại
    2. Đọc file CSV
    3. Chuyển đổi cột thời gian sang DateTime
    4. Kiểm tra và loại bỏ dữ liệu trùng/thiếu
    5. Chuẩn hóa và làm tròn số liệu
    6. Đổi tên cột sang Tiếng Việt
    7. Lưu file sạch
    
    Returns:
        Optional[pd.DataFrame]: DataFrame đã xử lý nếu thành công,
                                None nếu thất bại
                                
    Raises:
        FileNotFoundError: File dữ liệu thô không tồn tại
        pd.errors.ParserError: Lỗi đọc file CSV
        Exception: Các lỗi khác
        
    Examples:
        >>> df = clean_data()
        >>> print(df.columns.tolist())
        ['Thời Gian', 'Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió', 'Mô Tả']
    """
    
    print("🧹 Đang tiến hành làm sạch dữ liệu...")
    
    # ===== BƯỚC 1: KIỂM TRA FILE =====
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ LỖI: Không tìm thấy file dữ liệu thô")
        print(f"📁 Đường dẫn: {RAW_DATA_PATH}")
        print("💡 Vui lòng chạy cập nhật dữ liệu từ API trước")
        return None
    
    # ===== BƯỚC 2: ĐỌC DỮ LIỆU =====
    try:
        print(f"📖 Đang đọc file: {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8-sig')
        print(f"✓ Đã đọc {len(df)} dòng dữ liệu")
        
    except pd.errors.ParserError as e:
        print(f"❌ LỖI: Lỗi đọc file CSV - {e}")
        return None
    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy file: {RAW_DATA_PATH}")
        return None
    except Exception as e:
        print(f"❌ LỖI không xác định khi đọc file: {e}")
        return None
    
    # ===== BƯỚC 3: KIỂM TRA TRƯỜNG DỮ LIỆU =====
    required_columns = ['dt_txt', 'temp', 'humidity', 'pressure', 'wind_speed', 'description']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        print(f"❌ LỖI: Thiếu các cột: {missing_cols}")
        print(f"Các cột có sẵn: {df.columns.tolist()}")
        return None
    
    print(f"✓ Tất cả các cột bắt buộc đều có sẵn")
    
    # ===== BƯỚC 4: KIỂM TRA DỮ LIỆU THIẾU =====
    print("\n📋 Kiểm tra dữ liệu thiếu...")
    missing_info = df.isnull().sum()
    
    if missing_info.sum() > 0:
        print("⚠️ Phát hiện dữ liệu thiếu:")
        for col, count in missing_info[missing_info > 0].items():
            print(f"  - {col}: {count} dòng")
        
        # Xử lý dữ liệu thiếu
        df['pressure'] = df['pressure'].fillna(df['pressure'].mean())  # Điền giá trị trung bình
        df['wind_speed'] = df['wind_speed'].fillna(0)  # Điền 0 cho tốc gió
        df['description'] = df['description'].fillna('Không xác định')  # Điền văn bản
        
        print("✓ Đã xử lý dữ liệu thiếu (điền giá trị hợp lý)")
    else:
        print("✓ Không có dữ liệu thiếu")
    
    # ===== BƯỚC 5: KIỂM TRA TRÙNG LẶP =====
    print("\n🔍 Kiểm tra dữ liệu trùng lặp...")
    dup_before = len(df)
    df = df.drop_duplicates(subset=['dt_txt'], keep='first')  # Giữ bản ghi đầu tiên
    dup_count = dup_before - len(df)
    
    if dup_count > 0:
        print(f"⚠️ Phát hiện {dup_count} dòng trùng lặp (loại bỏ)")
    else:
        print("✓ Không có dữ liệu trùng lặp")
    
    # ===== BƯỚC 6: CHUYỂN ĐỔI THỜI GIAN =====
    print("\n⏰ Chuyển đổi cột thời gian...")
    try:
        df['dt_txt'] = pd.to_datetime(df['dt_txt'])
        print("✓ Chuyển đổi thành công sang định dạng DateTime")
    except Exception as e:
        print(f"❌ LỖI: Không thể chuyển đổi thời gian - {e}")
        return None
    
    # ===== BƯỚC 7: KIỂM TRA GIÁ TRỊ NGOẠI LỆ (OUTLIERS) =====
    print("\n⚠️ Kiểm tra giá trị ngoại lệ...")
    
    # Kiểm tra nhiệt độ
    invalid_temp = df[(df['temp'] < -100) | (df['temp'] > 70)]
    if len(invalid_temp) > 0:
        print(f"  - Tìm thấy {len(invalid_temp)} giá trị nhiệt độ ngoại lệ (loại bỏ)")
        df = df.drop(invalid_temp.index)
    
    # Kiểm tra độ ẩm
    invalid_humidity = df[(df['humidity'] < 0) | (df['humidity'] > 100)]
    if len(invalid_humidity) > 0:
        print(f"  - Tìm thấy {len(invalid_humidity)} giá trị độ ẩm ngoại lệ (loại bỏ)")
        df = df.drop(invalid_humidity.index)
    
    # Kiểm tra tốc gió
    invalid_wind = df[df['wind_speed'] < 0]
    if len(invalid_wind) > 0:
        print(f"  - Tìm thấy {len(invalid_wind)} giá trị tốc gió âm (loại bỏ)")
        df = df.drop(invalid_wind.index)
    
    if len(invalid_temp) == 0 and len(invalid_humidity) == 0 and len(invalid_wind) == 0:
        print("✓ Tất cả giá trị đều hợp lệ")
    
    # ===== BƯỚC 8: LÀM TRÒN SỐ LIỆU =====
    print("\n🔢 Làm tròn số liệu...")
    df['temp'] = df['temp'].round(1)
    df['humidity'] = df['humidity'].round(0).astype(int)
    df['pressure'] = df['pressure'].round(0).astype(int)
    df['wind_speed'] = df['wind_speed'].round(2)
    print("✓ Làm tròn hoàn tất")
    
    # ===== BƯỚC 9: ĐỔI TÊN CỘT SANG TIẾNG VIỆT =====
    print("\n🇻🇳 Đổi tên cột sang Tiếng Việt...")
    df = df.rename(columns={
        'dt_txt': 'Thời Gian',
        'temp': 'Nhiệt Độ',
        'humidity': 'Độ Ẩm',
        'pressure': 'Áp Suất',
        'wind_speed': 'Tốc Gió',
        'description': 'Mô Tả'
    })
    print(f"✓ Tên cột mới: {df.columns.tolist()}")
    
    # ===== BƯỚC 10: KIỂM TRA KÍCH THƯỚC DỮ LIỆU =====
    if len(df) == 0:
        print("❌ LỖI: Tất cả dữ liệu đã bị loại bỏ!")
        return None
    
    # ===== BƯỚC 11: LƯU FILE =====
    print(f"\n💾 Lưu file dữ liệu sạch...")
    try:
        os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
        df.to_csv(PROCESSED_DATA_PATH, index=False, encoding='utf-8-sig')
        
        print(f"✅ Thành công! Đã lưu dữ liệu sạch")
        print(f"📁 Vị trí file: {PROCESSED_DATA_PATH}")
        print(f"📊 Tổng bản ghi: {len(df)}")
        print(f"💾 Kích thước: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
    except IOError as e:
        print(f"❌ LỖI: Không thể lưu file - {e}")
        return None
    
    # ===== BƯỚC 12: HIỂN THỊ THỐNG KÊ =====
    print("\n📈 Thống kê dữ liệu:")
    print(f"{'Thời gian:':20} {df['Thời Gian'].min()} → {df['Thời Gian'].max()}")
    print(f"{'Nhiệt độ (°C):':20} Tối thiểu: {df['Nhiệt Độ'].min()}, Tối đa: {df['Nhiệt Độ'].max()}")
    print(f"{'Độ ẩm (%):':20} Tối thiểu: {df['Độ Ẩm'].min()}, Tối đa: {df['Độ Ẩm'].max()}")
    print(f"{'Áp suất (hPa):':20} Tối thiểu: {df['Áp Suất'].min()}, Tối đa: {df['Áp Suất'].max()}")
    
    # ===== HIỂN THỊ MẪU DỮ LIỆU =====
    print("\n📋 Mẫu dữ liệu (5 dòng đầu):")
    print(df.head(5).to_string(index=False))
    
    return df


if __name__ == "__main__":
    # Chạy thử
    df = clean_data()