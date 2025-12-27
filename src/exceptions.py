# src/exceptions.py
"""
Module định nghĩa các exception tùy chỉnh cho ứng dụng.

Mục đích:
    - Thay thế generic Exception bằng các exception cụ thể
    - Dễ dàng xử lý lỗi theo từng loại
    - Cung cấp thông báo lỗi rõ ràng

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""


class WeatherAppException(Exception):
    """Base exception cho tất cả các exception trong ứng dụng."""
    pass


class WeatherAPIError(WeatherAppException):
    """
    Exception cho các lỗi liên quan đến API.
    
    Bao gồm:
        - Lỗi kết nối
        - API key không hợp lệ
        - Response không hợp lệ
        - Timeout
    """
    
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"API Error [{self.status_code}]: {self.message}"
        return f"API Error: {self.message}"


class CityNotFoundError(WeatherAppException):
    """
    Exception khi thành phố không tồn tại trong danh sách.
    """
    
    def __init__(self, city_name: str, available_cities: list = None):
        self.city_name = city_name
        self.available_cities = available_cities
        
        message = f"Thành phố '{city_name}' không có trong danh sách"
        if available_cities:
            message += f". Các thành phố có sẵn: {', '.join(available_cities)}"
        
        super().__init__(message)


class DataValidationError(WeatherAppException):
    """
    Exception cho các lỗi validation dữ liệu.
    
    Bao gồm:
        - Giá trị ngoài phạm vi hợp lệ
        - Dữ liệu thiếu
        - Format không đúng
    """
    
    def __init__(self, message: str, field: str = None, value: any = None):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        if self.field and self.value is not None:
            return f"Validation Error [{self.field}={self.value}]: {self.message}"
        return f"Validation Error: {self.message}"


class DataProcessingError(WeatherAppException):
    """
    Exception cho các lỗi trong quá trình xử lý dữ liệu.
    
    Bao gồm:
        - Lỗi khi clean data
        - Lỗi khi transform data
        - Lỗi khi aggregate data
    """
    pass


class FileOperationError(WeatherAppException):
    """
    Exception cho các lỗi liên quan đến file operations.
    
    Bao gồm:
        - File không tồn tại
        - Không thể đọc file
        - Không thể ghi file
        - Permission denied
    """
    
    def __init__(self, message: str, filepath: str = None):
        self.filepath = filepath
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        if self.filepath:
            return f"File Operation Error [{self.filepath}]: {self.message}"
        return f"File Operation Error: {self.message}"


class ChartGenerationError(WeatherAppException):
    """
    Exception cho các lỗi khi tạo biểu đồ.
    
    Bao gồm:
        - Lỗi matplotlib
        - Thiếu dữ liệu để vẽ
        - Không thể lưu ảnh
    """
    
    def __init__(self, message: str, chart_type: str = None):
        self.chart_type = chart_type
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        if self.chart_type:
            return f"Chart Generation Error [{self.chart_type}]: {self.message}"
        return f"Chart Generation Error: {self.message}"


class EmptyDataFrameError(DataValidationError):
    """
    Exception khi DataFrame rỗng hoặc không có dữ liệu.
    """
    
    def __init__(self, message: str = "DataFrame rỗng hoặc không có dữ liệu"):
        super().__init__(message)


class MissingColumnError(DataValidationError):
    """
    Exception khi DataFrame thiếu cột bắt buộc.
    """
    
    def __init__(self, column_name: str, available_columns: list = None):
        self.column_name = column_name
        self.available_columns = available_columns
        
        message = f"Thiếu cột bắt buộc: '{column_name}'"
        if available_columns:
            message += f". Các cột hiện có: {', '.join(available_columns)}"
        
        super().__init__(message, field=column_name)
