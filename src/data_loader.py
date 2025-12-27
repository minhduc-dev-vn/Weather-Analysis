# src/data_loader.py
"""
Module lấy dữ liệu thời tiết từ API OpenWeatherMap.

Chức năng:
    - Kết nối API OpenWeatherMap
    - Tải dữ liệu dự báo 5 ngày
    - Lưu dữ liệu thô thành file CSV

Author: Weather Forecast Pro Team
Date: 2025-12-27 (Refactored for code quality)
"""

import requests
import pandas as pd
import os
from typing import Optional, Dict, Any, List

from .config import API_KEY, BASE_URL, VIETNAM_CITIES, DEFAULT_CITY_VIET, get_raw_data_path
from .constants import (
    API_TIMEOUT_SECONDS,
    MIN_VALID_TEMPERATURE, MAX_VALID_TEMPERATURE,
    MIN_VALID_HUMIDITY, MAX_VALID_HUMIDITY,
    EMOJI_LOADING, EMOJI_FILE, EMOJI_CHART
)
from .column_names import RawColumns
from .exceptions import WeatherAPIError, CityNotFoundError, DataValidationError, FileOperationError
from .logger import get_logger, log_success, log_error, log_warning, log_info


# Logger cho module này
logger = get_logger(__name__)


def _validate_api_key() -> None:
    """
    Kiểm tra API Key hợp lệ.
    
    Raises:
        WeatherAPIError: Nếu API Key chưa được cấu hình
    """
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        error_msg = "API Key chưa được cấu hình! Vui lòng thay thế API_KEY trong file src/config.py"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg)


def _validate_city_name(city_name_viet: str) -> str:
    """
    Kiểm tra và chuyển đổi tên thành phố.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
        
    Returns:
        str: Tên thành phố tiếng Anh (để gọi API)
        
    Raises:
        CityNotFoundError: Nếu thành phố không có trong danh sách
    """
    if city_name_viet not in VIETNAM_CITIES:
        log_error(f"Thành phố '{city_name_viet}' không có trong danh sách", logger)
        raise CityNotFoundError(city_name_viet, list(VIETNAM_CITIES.keys()))
    
    city_name_en = VIETNAM_CITIES[city_name_viet]
    logger.info(f"{EMOJI_LOADING} Chuẩn bị lấy dữ liệu cho: {city_name_viet} ({city_name_en})")
    return city_name_en


def _make_api_request(city_name_en: str) -> Dict[str, Any]:
    """
    Gửi request tới API và xử lý response.
    
    Args:
        city_name_en: Tên thành phố tiếng Anh
        
    Returns:
        Dict: JSON response từ API
        
    Raises:
        WeatherAPIError: Nếu có lỗi khi gọi API
    """
    url = f"{BASE_URL}?q={city_name_en}&appid={API_KEY}&units=metric&lang=vi"
    
    try:
        logger.info(f"Đang gửi request tới OpenWeatherMap API...")
        response = requests.get(url, timeout=API_TIMEOUT_SECONDS)
        
        # Xử lý các mã lỗi HTTP cụ thể
        if response.status_code == 401:
            error_msg = "API Key không hợp lệ hoặc đã hết hạn"
            log_error(f"Lỗi 401: {error_msg}", logger)
            raise WeatherAPIError(error_msg, status_code=401)
            
        elif response.status_code == 404:
            error_msg = f"Không tìm thấy thành phố: {city_name_en}"
            log_error(f"Lỗi 404: {error_msg}", logger)
            raise WeatherAPIError(error_msg, status_code=404)
            
        elif response.status_code == 429:
            error_msg = "Vượt giới hạn API (quá nhiều request). Vui lòng đợi vài phút"
            log_error(f"Lỗi 429: {error_msg}", logger)
            raise WeatherAPIError(error_msg, status_code=429)
        
        # Raise cho các mã lỗi khác
        response.raise_for_status()
        
        data = response.json()
        log_success("Nhận dữ liệu từ API thành công", logger)
        return data
        
    except requests.exceptions.Timeout:
        error_msg = f"Timeout sau {API_TIMEOUT_SECONDS} giây - API không phản hồi"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg) from None
        
    except requests.exceptions.ConnectionError:
        error_msg = "Không thể kết nối tới API - kiểm tra kết nối Internet"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg) from None
        
    except ValueError as e:
        error_msg = f"Dữ liệu trả về không phải JSON hợp lệ: {e}"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg) from e


def _validate_api_response(data: Dict[str, Any]) -> None:
    """
    Kiểm tra cấu trúc response từ API.
    
    Args:
        data: JSON response từ API
        
    Raises:
        WeatherAPIError: Nếu cấu trúc response không hợp lệ
    """
    if 'list' not in data:
        error_msg = "Dữ liệu trả về không đúng cấu trúc (thiếu 'list')"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg)
    
    if len(data['list']) == 0:
        error_msg = "Danh sách dự báo trống"
        log_error(error_msg, logger)
        raise WeatherAPIError(error_msg)
    
    if 'city' in data:
        city_name = data['city'].get('name', 'Unknown')
        logger.info(f"Dữ liệu cho thành phố: {city_name}")
    else:
        log_warning("Dữ liệu thiếu thông tin thành phố", logger)


def _validate_weather_record(record: Dict[str, Any], index: int) -> bool:
    """
    Kiểm tra một bản ghi thời tiết có hợp lệ không.
    
    Args:
        record: Dictionary chứa dữ liệu một mốc thời gian
        index: Index của bản ghi (để log)
        
    Returns:
        bool: True nếu hợp lệ, False nếu không hợp lệ
    """
    # Kiểm tra các trường bắt buộc
    required_fields = ['dt_txt', 'main', 'wind', 'weather']
    if not all(field in record for field in required_fields):
        log_warning(f"Bản ghi {index}: Thiếu trường dữ liệu bắt buộc", logger)
        return False
    
    # Kiểm tra các giá trị con
    if 'temp' not in record['main'] or 'humidity' not in record['main']:
        log_warning(f"Bản ghi {index}: Thiếu dữ liệu thời tiết", logger)
        return False
    
    # Kiểm tra nhiệt độ hợp lý
    temp = record['main']['temp']
    if not (MIN_VALID_TEMPERATURE <= temp <= MAX_VALID_TEMPERATURE):
        log_warning(f"Bản ghi {index}: Nhiệt độ {temp}°C ngoài phạm vi hợp lệ", logger)
        return False
    
    # Kiểm tra độ ẩm hợp lý
    humidity = record['main']['humidity']
    if not (MIN_VALID_HUMIDITY <= humidity <= MAX_VALID_HUMIDITY):
        log_warning(f"Bản ghi {index}: Độ ẩm {humidity}% ngoài phạm vi hợp lệ", logger)
        return False
    
    return True


def _extract_weather_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Trích xuất dữ liệu từ một bản ghi API.
    
    Args:
        record: Dictionary chứa dữ liệu từ API
        
    Returns:
        Dict: Dictionary chứa dữ liệu đã trích xuất
    """
    row = {
        RawColumns.DT_TXT.value: record['dt_txt'],
        RawColumns.TEMP.value: record['main']['temp'],
        RawColumns.FEELS_LIKE.value: record['main'].get('feels_like', record['main']['temp']),
        RawColumns.HUMIDITY.value: record['main']['humidity'],
        RawColumns.PRESSURE.value: record['main'].get('pressure', None),
        RawColumns.WIND_SPEED.value: record['wind'].get('speed', 0),
        RawColumns.WIND_DEG.value: record['wind'].get('deg', None),
        RawColumns.CLOUDS.value: record.get('clouds', {}).get('all', None) if isinstance(record.get('clouds'), dict) else record.get('clouds', None),
        RawColumns.VISIBILITY.value: record.get('visibility', None),
        RawColumns.DESCRIPTION.value: record['weather'][0]['description'] if record['weather'] else 'Không xác định'
    }
    
    # Chuyển đổi visibility từ mét sang km
    if row[RawColumns.VISIBILITY.value] is not None:
        row[RawColumns.VISIBILITY.value] = row[RawColumns.VISIBILITY.value] / 1000.0
    
    return row


def _parse_weather_data(data: Dict[str, Any], city_name_viet: str) -> pd.DataFrame:
    """
    Parse dữ liệu từ API response thành DataFrame.
    
    Args:
        data: JSON response từ API
        city_name_viet: Tên thành phố tiếng Việt
        
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu thời tiết
        
    Raises:
        DataValidationError: Nếu không có bản ghi hợp lệ
    """
    weather_list = data['list']
    rows = []
    invalid_count = 0
    
    logger.info(f"Đang xử lý {len(weather_list)} bản ghi dữ liệu...")
    
    for idx, record in enumerate(weather_list):
        try:
            # Validate record
            if not _validate_weather_record(record, idx):
                invalid_count += 1
                continue
            
            # Extract data
            row = _extract_weather_record(record)
            rows.append(row)
            
        except (KeyError, IndexError, TypeError) as e:
            log_warning(f"Bản ghi {idx}: Lỗi xử lý - {e}", logger)
            invalid_count += 1
            continue
    
    # Kiểm tra có dữ liệu hợp lệ không
    if len(rows) == 0:
        error_msg = "Không có bản ghi hợp lệ sau khi xử lý"
        log_error(error_msg, logger)
        raise DataValidationError(error_msg)
    
    # Tạo DataFrame
    df = pd.DataFrame(rows)
    
    # Log kết quả
    if invalid_count > 0:
        log_warning(f"Loại bỏ {invalid_count} bản ghi không hợp lệ", logger)
    log_success(f"Giữ lại {len(df)} bản ghi hợp lệ", logger)
    
    # Loại bỏ duplicate
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        log_warning(f"Phát hiện {dup_count} bản ghi trùng lặp (đang loại bỏ)", logger)
        df = df.drop_duplicates()
    
    # Thêm cột thành phố
    df[RawColumns.CITY_NAME.value] = city_name_viet
    
    return df


def _save_raw_data(df: pd.DataFrame, filepath: str) -> None:
    """
    Lưu DataFrame thành file CSV.
    
    Args:
        df: DataFrame cần lưu
        filepath: Đường dẫn file output
        
    Raises:
        FileOperationError: Nếu không thể lưu file
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        file_size = df.memory_usage(deep=True).sum() / 1024
        log_success(f"Đã lưu {len(df)} dòng dữ liệu", logger)
        logger.info(f"{EMOJI_FILE} Vị trí: {filepath}")
        logger.info(f"{EMOJI_CHART} Kích thước: {file_size:.2f} KB")
        
    except PermissionError as e:
        error_msg = f"Không có quyền ghi file: {filepath}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e
        
    except IOError as e:
        error_msg = f"Lỗi I/O khi lưu file CSV: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e


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
        - visibility: Tầm nhìn (km)
        - description: Mô tả thời tiết
        - city_name: Tên thành phố
        
    Raises:
        WeatherAPIError: Lỗi liên quan đến API
        CityNotFoundError: Thành phố không tồn tại
        DataValidationError: Dữ liệu không hợp lệ
        FileOperationError: Lỗi khi lưu file
        
    Examples:
        >>> df = fetch_weather_data("Hà Nội")
        >>> print(df.shape)
        (40, 11)
    """
    
    try:
        # 1. Validate API Key
        _validate_api_key()
        
        # 2. Validate và chuyển đổi tên thành phố
        city_name_en = _validate_city_name(city_name_viet)
        
        # 3. Gửi request tới API
        data = _make_api_request(city_name_en)
        
        # 4. Validate response structure
        _validate_api_response(data)
        
        # 5. Parse dữ liệu
        df = _parse_weather_data(data, city_name_viet)
        
        # 6. Lưu file
        raw_data_path = get_raw_data_path(city_name_viet)
        _save_raw_data(df, raw_data_path)
        
        return df
        
    except (WeatherAPIError, CityNotFoundError, DataValidationError, FileOperationError) as e:
        # Các exception cụ thể đã được log bên trong, chỉ cần return None
        logger.error(f"Lỗi khi lấy dữ liệu: {e}")
        return None
        
    except Exception as e:
        # Lỗi không mong đợi
        log_error(f"Lỗi không xác định: {type(e).__name__}: {e}", logger, exc_info=True)
        return None


def fetch_multiple_cities(city_list: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """
    Lấy dữ liệu thời tiết cho nhiều thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt. Nếu None thì lấy tất cả.
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary với key là tên thành phố, value là DataFrame
        
    Example:
        >>> results = fetch_multiple_cities(['Hà Nội', 'TP. Hồ Chí Minh'])
        >>> print(len(results))
        2
    """
    if city_list is None:
        city_list = list(VIETNAM_CITIES.keys())
    
    logger.info(f"Bắt đầu lấy dữ liệu cho {len(city_list)} thành phố...")
    
    results = {}
    for city in city_list:
        logger.info(f"\n{'='*50}")
        logger.info(f"Đang xử lý: {city}")
        logger.info(f"{'='*50}")
        
        df = fetch_weather_data(city)
        if df is not None:
            results[city] = df
        else:
            log_warning(f"Không lấy được dữ liệu cho {city}", logger)
    
    log_success(f"Hoàn thành! Lấy được dữ liệu cho {len(results)}/{len(city_list)} thành phố", logger)
    return results


if __name__ == "__main__":
    # Test code
    df = fetch_weather_data("Hà Nội")
    if df is not None:
        logger.info("\nDữ liệu mẫu (5 dòng đầu):")
        logger.info(f"\n{df.head()}")
        logger.info(f"\nCác cột: {df.columns.tolist()}")