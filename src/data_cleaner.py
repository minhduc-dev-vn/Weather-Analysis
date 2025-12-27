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
Date: 2025-12-27 (Refactored for code quality)
"""

import pandas as pd
import os
from typing import Optional, List

from .config import DEFAULT_CITY_VIET, get_raw_data_path, get_processed_data_path
from .constants import (
    MIN_VALID_TEMPERATURE, MAX_VALID_TEMPERATURE,
    MIN_VALID_HUMIDITY, MAX_VALID_HUMIDITY,
    MIN_VALID_WIND_SPEED,
    MISSING_VALUE_THRESHOLD,
    EMOJI_FILE, EMOJI_CHART
)
from .column_names import RawColumns, CleanColumns, rename_to_clean
from .exceptions import FileOperationError, DataValidationError, DataProcessingError, EmptyDataFrameError
from .logger import get_logger, log_success, log_error, log_warning, log_info


# Logger cho module này
logger = get_logger(__name__)


def _validate_file_exists(filepath: str) -> None:
    """
    Kiểm tra file dữ liệu thô tồn tại.
    
    Args:
        filepath: Đường dẫn file cần kiểm tra
        
    Raises:
        FileOperationError: Nếu file không tồn tại
    """
    if not os.path.exists(filepath):
        error_msg = f"Không tìm thấy file dữ liệu thô: {filepath}. Vui lòng chạy cập nhật dữ liệu từ API trước."
        log_error(error_msg, logger)
        raise FileOperationError(error_msg, filepath)


def _load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Đọc dữ liệu từ file CSV.
    
    Args:
        filepath: Đường dẫn file CSV
        
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu thô
        
    Raises:
        FileOperationError: Nếu không thể đọc file
    """
    try:
        logger.info(f"Đang đọc file: {filepath}")
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        log_success(f"Đã đọc {len(df)} dòng dữ liệu", logger)
        return df
        
    except pd.errors.ParserError as e:
        error_msg = f"Lỗi parse CSV: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e
        
    except Exception as e:
        error_msg = f"Lỗi không xác định khi đọc file: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Kiểm tra các cột bắt buộc phải có.
    
    Args:
        df: DataFrame cần kiểm tra
        
    Raises:
        DataValidationError: Nếu thiếu cột bắt buộc
    """
    required_columns = [
        RawColumns.DT_TXT.value,
        RawColumns.TEMP.value,
        RawColumns.HUMIDITY.value,
        RawColumns.PRESSURE.value,
        RawColumns.WIND_SPEED.value,
        RawColumns.DESCRIPTION.value
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        error_msg = f"Thiếu các cột bắt buộc: {missing_cols}. Các cột hiện có: {df.columns.tolist()}"
        log_error(error_msg, logger)
        raise DataValidationError(error_msg)
    
    log_success("Tất cả các cột bắt buộc đều có sẵn", logger)


def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xử lý dữ liệu thiếu (missing values).
    
    Args:
        df: DataFrame cần xử lý
        
    Returns:
        pd.DataFrame: DataFrame đã được xử lý missing values
    """
    logger.info("Kiểm tra dữ liệu thiếu...")
    missing_info = df.isnull().sum()
    
    if missing_info.sum() > 0:
        log_warning("Phát hiện dữ liệu thiếu:", logger)
        for col, count in missing_info[missing_info > 0].items():
            logger.warning(f"  - {col}: {count} dòng")
        
        # Điền giá trị cho các cột cụ thể
        if RawColumns.PRESSURE.value in df.columns:
            df[RawColumns.PRESSURE.value] = df[RawColumns.PRESSURE.value].fillna(
                df[RawColumns.PRESSURE.value].mean()
            )
        
        if RawColumns.WIND_SPEED.value in df.columns:
            df[RawColumns.WIND_SPEED.value] = df[RawColumns.WIND_SPEED.value].fillna(0)
        
        if RawColumns.DESCRIPTION.value in df.columns:
            df[RawColumns.DESCRIPTION.value] = df[RawColumns.DESCRIPTION.value].fillna('Không xác định')
        
        # Xử lý các cột optional
        if RawColumns.FEELS_LIKE.value in df.columns:
            df[RawColumns.FEELS_LIKE.value] = df[RawColumns.FEELS_LIKE.value].fillna(
                df[RawColumns.TEMP.value]
            )
        
        if RawColumns.WIND_DEG.value in df.columns:
            df[RawColumns.WIND_DEG.value] = df[RawColumns.WIND_DEG.value].fillna(
                df[RawColumns.WIND_DEG.value].median()
            )
        
        if RawColumns.CLOUDS.value in df.columns:
            df[RawColumns.CLOUDS.value] = df[RawColumns.CLOUDS.value].fillna(
                df[RawColumns.CLOUDS.value].median()
            )
        
        if RawColumns.VISIBILITY.value in df.columns:
            df[RawColumns.VISIBILITY.value] = df[RawColumns.VISIBILITY.value].fillna(
                df[RawColumns.VISIBILITY.value].median()
            )
        
        log_success("Đã xử lý dữ liệu thiếu (điền giá trị hợp lý)", logger)
    else:
        log_success("Không có dữ liệu thiếu", logger)
    
    return df


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Loại bỏ dữ liệu trùng lặp.
    
    Args:
        df: DataFrame cần xử lý
        
    Returns:
        pd.DataFrame: DataFrame đã loại bỏ duplicate
    """
    logger.info("Kiểm tra dữ liệu trùng lặp...")
    dup_before = len(df)
    df = df.drop_duplicates(subset=[RawColumns.DT_TXT.value], keep='first')
    dup_count = dup_before - len(df)
    
    if dup_count > 0:
        log_warning(f"Phát hiện {dup_count} dòng trùng lặp (đã loại bỏ)", logger)
    else:
        log_success("Không có dữ liệu trùng lặp", logger)
    
    return df


def _convert_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển đổi cột thời gian sang DateTime.
    
    Args:
        df: DataFrame cần xử lý
        
    Returns:
        pd.DataFrame: DataFrame với cột thời gian đã được chuyển đổi
        
    Raises:
        DataProcessingError: Nếu không thể chuyển đổi
    """
    logger.info("Chuyển đổi cột thời gian...")
    try:
        df[RawColumns.DT_TXT.value] = pd.to_datetime(df[RawColumns.DT_TXT.value])
        log_success("Chuyển đổi thành công sang định dạng DateTime", logger)
        return df
        
    except Exception as e:
        error_msg = f"Không thể chuyển đổi thời gian: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise DataProcessingError(error_msg) from e


def _validate_data_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kiểm tra và loại bỏ giá trị ngoại lệ (outliers).
    
    Args:
        df: DataFrame cần kiểm tra
        
    Returns:
        pd.DataFrame: DataFrame đã loại bỏ outliers
    """
    logger.info("Kiểm tra giá trị ngoại lệ...")
    
    initial_len = len(df)
    
    # Kiểm tra nhiệt độ
    temp_col = RawColumns.TEMP.value
    invalid_temp = df[(df[temp_col] < MIN_VALID_TEMPERATURE) | (df[temp_col] > MAX_VALID_TEMPERATURE)]
    if len(invalid_temp) > 0:
        log_warning(f"Tìm thấy {len(invalid_temp)} giá trị nhiệt độ ngoại lệ (loại bỏ)", logger)
        df = df.drop(invalid_temp.index)
    
    # Kiểm tra độ ẩm
    humidity_col = RawColumns.HUMIDITY.value
    invalid_humidity = df[(df[humidity_col] < MIN_VALID_HUMIDITY) | (df[humidity_col] > MAX_VALID_HUMIDITY)]
    if len(invalid_humidity) > 0:
        log_warning(f"Tìm thấy {len(invalid_humidity)} giá trị độ ẩm ngoại lệ (loại bỏ)", logger)
        df = df.drop(invalid_humidity.index)
    
    # Kiểm tra tốc gió
    wind_col = RawColumns.WIND_SPEED.value
    invalid_wind = df[df[wind_col] < MIN_VALID_WIND_SPEED]
    if len(invalid_wind) > 0:
        log_warning(f"Tìm thấy {len(invalid_wind)} giá trị tốc gió âm (loại bỏ)", logger)
        df = df.drop(invalid_wind.index)
    
    removed = initial_len - len(df)
    if removed == 0:
        log_success("Tất cả giá trị đều hợp lệ", logger)
    else:
        logger.info(f"Đã loại bỏ tổng {removed} bản ghi ngoại lệ")
    
    return df


def _round_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Làm tròn các giá trị số.
    
    Args:
        df: DataFrame cần xử lý
        
    Returns:
        pd.DataFrame: DataFrame với các giá trị đã được làm tròn
    """
    logger.info("Làm tròn số liệu...")
    
    # Làm tròn các cột bắt buộc
    df[RawColumns.TEMP.value] = df[RawColumns.TEMP.value].round(1)
    df[RawColumns.HUMIDITY.value] = df[RawColumns.HUMIDITY.value].round(0).astype(int)
    df[RawColumns.PRESSURE.value] = df[RawColumns.PRESSURE.value].round(0).astype(int)
    df[RawColumns.WIND_SPEED.value] = df[RawColumns.WIND_SPEED.value].round(2)
    
    # Làm tròn các cột optional nếu có
    if RawColumns.FEELS_LIKE.value in df.columns:
        df[RawColumns.FEELS_LIKE.value] = df[RawColumns.FEELS_LIKE.value].round(1)
    
    if RawColumns.WIND_DEG.value in df.columns:
        df[RawColumns.WIND_DEG.value] = df[RawColumns.WIND_DEG.value].round(0).astype(int)
    
    if RawColumns.CLOUDS.value in df.columns:
        df[RawColumns.CLOUDS.value] = df[RawColumns.CLOUDS.value].round(0).astype(int)
    
    if RawColumns.VISIBILITY.value in df.columns:
        df[RawColumns.VISIBILITY.value] = df[RawColumns.VISIBILITY.value].round(2)
    
    log_success("Làm tròn hoàn tất", logger)
    return df


def _rename_columns_vietnamese(df: pd.DataFrame) -> pd.DataFrame:
    """
    Đổi tên cột sang tiếng Việt.
    
    Args:
        df: DataFrame cần đổi tên cột
        
    Returns:
        pd.DataFrame: DataFrame với tên cột tiếng Việt
    """
    logger.info("Đổi tên cột sang Tiếng Việt...")
    
    # Sử dụng mapping function từ column_names
    rename_dict = rename_to_clean(df.columns.tolist())
    df = df.rename(columns=rename_dict)
    
    logger.info(f"Tên cột mới: {df.columns.tolist()}")
    return df


def _save_processed_data(df: pd.DataFrame, filepath: str) -> None:
    """
    Lưu DataFrame đã xử lý thành file CSV.
    
    Args:
        df: DataFrame cần lưu
        filepath: Đường dẫn file output
        
    Raises:
        FileOperationError: Nếu không thể lưu file
    """
    logger.info("Lưu file dữ liệu sạch...")
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        file_size = df.memory_usage(deep=True).sum() / 1024
        log_success("Đã lưu dữ liệu sạch", logger)
        logger.info(f"{EMOJI_FILE} Vị trí: {filepath}")
        logger.info(f"{EMOJI_CHART} Tổng bản ghi: {len(df)}")
        logger.info(f"{EMOJI_CHART} Kích thước: {file_size:.2f} KB")
        
    except PermissionError as e:
        error_msg = f"Không có quyền ghi file: {filepath}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e
        
    except IOError as e:
        error_msg = f"Lỗi I/O khi lưu file: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise FileOperationError(error_msg, filepath) from e


def _log_data_statistics(df: pd.DataFrame) -> None:
    """
    Log thống kê dữ liệu.
    
    Args:
        df: DataFrame cần thống kê
    """
    logger.info("\n📈 Thống kê dữ liệu:")
    logger.info(f"{'Thời gian:':20} {df[CleanColumns.THOI_GIAN.value].min()} → {df[CleanColumns.THOI_GIAN.value].max()}")
    logger.info(f"{'Nhiệt độ (°C):':20} Min: {df[CleanColumns.NHIET_DO.value].min()}, Max: {df[CleanColumns.NHIET_DO.value].max()}")
    logger.info(f"{'Độ ẩm (%):':20} Min: {df[CleanColumns.DO_AM.value].min()}, Max: {df[CleanColumns.DO_AM.value].max()}")
    logger.info(f"{'Áp suất (hPa):':20} Min: {df[CleanColumns.AP_SUAT.value].min()}, Max: {df[CleanColumns.AP_SUAT.value].max()}")
    
    # Hiển thị mẫu dữ liệu
    logger.info("\n📋 Mẫu dữ liệu (5 dòng đầu):")
    logger.info(f"\n{df.head(5).to_string(index=False)}")


def clean_data(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[pd.DataFrame]:
    """
    Đọc, xử lý và làm sạch dữ liệu thời tiết.
    
    Quy trình xử lý:
    1. Kiểm tra file dữ liệu thô tồn tại
    2. Đọc file CSV
    3. Validate các cột bắt buộc
    4. Xử lý dữ liệu thiếu
    5. Loại bỏ dữ liệu trùng lặp
    6. Chuyển đổi cột thời gian sang DateTime
    7. Kiểm tra và loại bỏ giá trị ngoại lệ
    8. Làm tròn số liệu
    9. Đổi tên cột sang Tiếng Việt
    10. Lưu file sạch
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[pd.DataFrame]: DataFrame đã xử lý nếu thành công,
                                None nếu thất bại
                                
    Raises:
        FileOperationError: Lỗi file operations
        DataValidationError: Dữ liệu không hợp lệ
        DataProcessingError: Lỗi xử lý dữ liệu
        EmptyDataFrameError: DataFrame rỗng
        
    Examples:
        >>> df = clean_data("Hà Nội")
        >>> print(df.columns.tolist())
        ['Thời Gian', 'Nhiệt Độ', 'Nhiệt Độ Cảm Nhận', 'Độ Ẩm', ...]
    """
    
    raw_data_path = get_raw_data_path(city_name_viet)
    processed_data_path = get_processed_data_path(city_name_viet)
    
    logger.info(f"🧹 Bắt đầu làm sạch dữ liệu cho: {city_name_viet}")
    
    try:
        # 1. Validate file tồn tại
        _validate_file_exists(raw_data_path)
        
        # 2. Đọc dữ liệu
        df = _load_raw_data(raw_data_path)
        
        # 3. Validate cột bắt buộc
        _validate_required_columns(df)
        
        # 4. Xử lý missing values
        df = _handle_missing_values(df)
        
        # 5. Loại bỏ duplicate
        df = _remove_duplicates(df)
        
        # 6. Chuyển đổi datetime
        df = _convert_datetime_column(df)
        
        # 7. Validate ranges và loại bỏ outliers
        df = _validate_data_ranges(df)
        
        # 8. Kiểm tra DataFrame không rỗng
        if len(df) == 0:
            error_msg = "Tất cả dữ liệu đã bị loại bỏ sau khi clean!"
            log_error(error_msg, logger)
            raise EmptyDataFrameError(error_msg)
        
        # 9. Làm tròn số liệu
        df = _round_numeric_values(df)
        
        # 10. Đổi tên cột sang tiếng Việt
        df = _rename_columns_vietnamese(df)
        
        # 11. Lưu file
        _save_processed_data(df, processed_data_path)
        
        # 12. Log statistics
        _log_data_statistics(df)
        
        return df
        
    except (FileOperationError, DataValidationError, DataProcessingError, EmptyDataFrameError) as e:
        logger.error(f"Lỗi khi clean data: {e}")
        return None
        
    except Exception as e:
        log_error(f"Lỗi không xác định: {type(e).__name__}: {e}", logger, exc_info=True)
        return None


if __name__ == "__main__":
    # Test code
    df = clean_data("Hà Nội")
    if df is not None:
        logger.info("✅ Test thành công!")