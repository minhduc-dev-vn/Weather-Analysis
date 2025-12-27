# src/data_loader.py
"""
Module lấy dữ liệu thời tiết từ API OpenWeatherMap.

Chức năng:
    - Kết nối API OpenWeatherMap
    - Tải dữ liệu dự báo 5 ngày
    - Lưu dữ liệu thô thành file CSV

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import requests
import pandas as pd
import os
from typing import Optional
from .config import API_KEY, BASE_URL, VIETNAM_CITIES, DEFAULT_CITY_VIET, get_raw_data_path


def fetch_weather_data(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[pd.DataFrame]:
    """
    Lấy dữ liệu thời tiết từ API OpenWeatherMap và lưu thành CSV.
    
    Hàm này thực hiện các bước:
    1. Xác thực API Key
    2. Gửi request tới API với thành phố được chỉ định
    3. Xử lý response JSON
    4. Chuyển đổi thành DataFrame với nhiều metric
    5. Lưu file CSV thô
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[pd.DataFrame]: DataFrame chứa dữ liệu thô nếu thành công, 
                                None nếu thất bại
                                
    Columns trong DataFrame trả về:
        - dt_txt: Thời gian dự báo (YYYY-MM-DD HH:MM:SS)
        - temp: Nhiệt độ (°C)
        - feels_like: Nhiệt độ cảm nhận (°C)
        - humidity: Độ ẩm (%)
        - pressure: Áp suất (hPa)
        - wind_speed: Tốc gió (m/s)
        - wind_deg: Hướng gió (độ)
        - clouds: Độ che phủ mây (%)
        - visibility: Tầm nhìn (m)
        - description: Mô tả thời tiết
        
    Raises:
        requests.exceptions.HTTPError: Lỗi HTTP từ API (sai API Key, không tìm thấy thành phố)
        requests.exceptions.ConnectionError: Lỗi kết nối mạng
        Exception: Các lỗi khác
        
    Examples:
        >>> df = fetch_weather_data("Hà Nội")
        >>> print(df.shape)
        (40, 10)
    """
    
    # Chuyển đổi tên thành phố
    if city_name_viet not in VIETNAM_CITIES:
        print(f"❌ LỖI: Thành phố '{city_name_viet}' không có trong danh sách")
        print(f"💡 Các thành phố có sẵn: {list(VIETNAM_CITIES.keys())}")
        return None
    
    city_name_en = VIETNAM_CITIES[city_name_viet]
    raw_data_path = get_raw_data_path(city_name_viet)
    
    print(f"📡 Đang kết nối API lấy dữ liệu cho: {city_name_viet} ({city_name_en})...")
    
    # ===== KIỂM THỰC API KEY =====
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("❌ LỖI: API Key chưa được cấu hình!")
        print("💡 Vui lòng thay thế API_KEY trong file src/config.py")
        return None
    
    # ===== TẠO URL =====
    url = f"{BASE_URL}?q={city_name_en}&appid={API_KEY}&units=metric&lang=vi"
    
    try:
        # ===== GỬI REQUEST =====
        print(f"🌐 Gửi request tới: {BASE_URL}...")
        response = requests.get(url, timeout=10)  # Timeout 10 giây
        
        # ===== KIỂM TRA STATUS CODE =====
        if response.status_code == 401:
            print("❌ LỖI 401: API Key không hợp lệ hoặc đã hết hạn")
            print("💡 Kiểm tra lại API Key trong file src/config.py")
            return None
        elif response.status_code == 404:
            print(f"❌ LỖI 404: Không tìm thấy thành phố '{city_name_en}' ({city_name_viet})")
            print("💡 Vui lòng kiểm tra tên thành phố")
            return None
        elif response.status_code == 429:
            print("❌ LỖI 429: Vượt giới hạn API (quá nhiều request)")
            print("💡 Vui lòng đợi vài phút rồi thử lại")
            return None
        else:
            response.raise_for_status()  # Báo lỗi nếu status code khác 200
        
        # ===== PARSE JSON =====
        data = response.json()
        
        # ===== KIỂM TRA CẤU TRÚC DỮ LIỆU =====
        if 'list' not in data:
            print("❌ LỖI: Dữ liệu trả về không đúng cấu trúc (thiếu 'list')")
            print(f"Response: {data}")
            return None
        
        if 'city' not in data:
            print("⚠️ CẢNH BÁO: Dữ liệu thiếu thông tin thành phố")
        else:
            city_info = data['city']['name']
            print(f"✓ Dữ liệu cho thành phố: {city_info}")
        
        weather_list = data['list']
        
        if len(weather_list) == 0:
            print("❌ LỖI: Danh sách dự báo trống")
            return None
        
        # ===== TRÍCH XUẤT DỮ LIỆU =====
        rows = []
        invalid_count = 0
        
        for idx, item in enumerate(weather_list):
            try:
                # Kiểm tra các trường bắt buộc
                if not all(k in item for k in ['dt_txt', 'main', 'wind', 'weather']):
                    print(f"⚠️ Bản ghi {idx}: Thiếu trường dữ liệu")
                    invalid_count += 1
                    continue
                
                # Kiểm tra các giá trị con
                if 'temp' not in item['main'] or 'humidity' not in item['main']:
                    print(f"⚠️ Bản ghi {idx}: Thiếu dữ liệu thời tiết")
                    invalid_count += 1
                    continue
                
                # Trích xuất dữ liệu với nhiều metric hơn
                row = {
                    'dt_txt': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'feels_like': item['main'].get('feels_like', item['main']['temp']),  # Nhiệt độ cảm nhận
                    'humidity': item['main']['humidity'],
                    'pressure': item['main'].get('pressure', None),
                    'wind_speed': item['wind'].get('speed', 0),
                    'wind_deg': item['wind'].get('deg', None),  # Hướng gió (0-360 độ)
                    'clouds': item.get('clouds', {}).get('all', None) if isinstance(item.get('clouds'), dict) else item.get('clouds', None),  # Độ che phủ mây (%)
                    'visibility': item.get('visibility', None),  # Tầm nhìn (mét), chia 1000 để có km
                    'description': item['weather'][0]['description'] if item['weather'] else 'Không xác định'
                }
                
                # Chuyển đổi visibility từ mét sang km nếu có
                if row['visibility'] is not None:
                    row['visibility'] = row['visibility'] / 1000.0  # Chuyển sang km
                
                # Kiểm tra nhiệt độ hợp lý (giới hạn vật lý)
                if row['temp'] < -100 or row['temp'] > 70:
                    print(f"⚠️ Bản ghi {idx}: Nhiệt độ {row['temp']}°C không hợp lý (loại bỏ)")
                    invalid_count += 1
                    continue
                
                # Kiểm tra độ ẩm hợp lý
                if not (0 <= row['humidity'] <= 100):
                    print(f"⚠️ Bản ghi {idx}: Độ ẩm {row['humidity']}% không hợp lý (loại bỏ)")
                    invalid_count += 1
                    continue
                
                rows.append(row)
                
            except (KeyError, IndexError, TypeError) as e:
                print(f"⚠️ Bản ghi {idx}: Lỗi xử lý - {e}")
                invalid_count += 1
                continue
        
        # ===== TẠO DATAFRAME =====
        if len(rows) == 0:
            print("❌ LỖI: Không có bản ghi hợp lệ sau khi xử lý")
            return None
        
        df = pd.DataFrame(rows)
        
        if invalid_count > 0:
            print(f"⚠️ Cảnh báo: Loại bỏ {invalid_count} bản ghi không hợp lệ")
            print(f"✓ Giữ lại {len(df)} bản ghi hợp lệ")
        
        # ===== KIỂM TRA TRÙNG LẶP =====
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            print(f"⚠️ Cảnh báo: Phát hiện {dup_count} bản ghi trùng lặp (loại bỏ)")
            df = df.drop_duplicates()
        
        # ===== THÊM CỘT THÀNH PHỐ =====
        df['city_name'] = city_name_viet
        
        # ===== LƯU FILE =====
        try:
            os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
            df.to_csv(raw_data_path, index=False, encoding='utf-8-sig')
            print(f"✅ Thành công! Đã lưu {len(df)} dòng dữ liệu")
            print(f"📁 Vị trí file: {raw_data_path}")
            print(f"📊 Kích thước: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            return df
            
        except IOError as e:
            print(f"❌ LỖI: Không thể lưu file CSV - {e}")
            return None
    
    # ===== XỪNG LỖI KẾT NỐI MẠNG =====
    except requests.exceptions.Timeout:
        print("❌ LỖI: Timeout - API không phản hồi (quá chậm)")
        print("💡 Kiểm tra kết nối mạng hoặc thử lại sau")
        return None
        
    except requests.exceptions.ConnectionError:
        print("❌ LỖI: Không thể kết nối tới API")
        print("💡 Kiểm tra kết nối Internet hoặc API server")
        return None
    
    # ===== XỨNG LỖI JSON =====
    except ValueError as e:
        print(f"❌ LỖI: Dữ liệu trả về không phải JSON hợp lệ - {e}")
        return None
    
    # ===== XỨNG LỖI CHUNG =====
    except Exception as e:
        print(f"❌ LỖI không xác định: {type(e).__name__}: {e}")
        return None


def fetch_multiple_cities(city_list: list = None) -> dict:
    """
    Lấy dữ liệu thời tiết cho nhiều thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt. Nếu None thì lấy tất cả.
    
    Returns:
        dict: Dictionary với key là tên thành phố, value là DataFrame
    """
    if city_list is None:
        city_list = list(VIETNAM_CITIES.keys())
    
    results = {}
    for city in city_list:
        print(f"\n{'='*50}")
        print(f"Đang xử lý: {city}")
        print(f"{'='*50}")
        df = fetch_weather_data(city)
        if df is not None:
            results[city] = df
        else:
            print(f"⚠️ Không lấy được dữ liệu cho {city}")
    
    return results


if __name__ == "__main__":
    # Chạy thử
    df = fetch_weather_data("Hà Nội")
    if df is not None:
        print("\nDữ liệu mẫu (5 dòng đầu):")
        print(df.head())
        print(f"\nCác cột: {df.columns.tolist()}")