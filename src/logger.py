# src/logger.py
"""
Module cấu hình logging cho toàn bộ ứng dụng.

Mục đích:
    - Thay thế print() bằng logging chuyên nghiệp
    - Hỗ trợ emoji và tiếng Việt
    - Ghi log ra console và file
    - Dễ dàng điều chỉnh log level

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .constants import (
    LOG_FILENAME, LOG_MAX_BYTES, LOG_BACKUP_COUNT,
    LOG_FORMAT, LOG_DATE_FORMAT,
    EMOJI_SUCCESS, EMOJI_ERROR, EMOJI_WARNING, EMOJI_INFO
)

# Tạo logger chính cho ứng dụng
_app_logger = None


class ColoredFormatter(logging.Formatter):
    """
    Formatter có màu sắc cho console output.
    Sử dụng ANSI color codes.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    # Emoji mapping
    EMOJI_MAP = {
        'DEBUG': '🔍',
        'INFO': EMOJI_INFO,
        'WARNING': EMOJI_WARNING,
        'ERROR': EMOJI_ERROR,
        'CRITICAL': '🚨'
    }
    
    def format(self, record):
        # Thêm emoji vào message
        emoji = self.EMOJI_MAP.get(record.levelname, '')
        
        # Tạo message với màu
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format gốc
        original_format = self._style._fmt
        
        # Thêm màu vào levelname
        colored_levelname = f"{color}{record.levelname}{reset}"
        
        # Tạo format mới với emoji và màu
        self._style._fmt = original_format.replace(
            '%(levelname)s',
            f'{emoji} {colored_levelname}'
        )
        
        result = super().format(record)
        
        # Khôi phục format gốc
        self._style._fmt = original_format
        
        return result


def setup_logger(
    name: str = 'WeatherApp',
    log_file: str = LOG_FILENAME,
    level: int = logging.INFO,
    console_output: bool = True,
    file_output: bool = True
) -> logging.Logger:
    """
    Thiết lập logger với cấu hình đầy đủ.
    
    Args:
        name: Tên logger
        log_file: Đường dẫn file log
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Có ghi ra console không
        file_output: Có ghi ra file không
        
    Returns:
        logging.Logger: Logger đã được cấu hình
        
    Example:
        >>> logger = setup_logger('MyModule')
        >>> logger.info('Thông báo thành công')
        >>> logger.error('Có lỗi xảy ra')
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Xóa handlers cũ nếu có (tránh duplicate)
    if logger.handlers:
        logger.handlers.clear()
    
    # ===== CONSOLE HANDLER =====
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Sử dụng ColoredFormatter cho console
        console_formatter = ColoredFormatter(
            fmt='%(message)s',  # Chỉ hiển thị message cho console (ngắn gọn hơn)
            datefmt=LOG_DATE_FORMAT
        )
        console_handler.setFormatter(console_formatter)
        
        # Đảm bảo UTF-8 encoding
        if hasattr(console_handler.stream, 'reconfigure'):
            console_handler.stream.reconfigure(encoding='utf-8')
        
        logger.addHandler(console_handler)
    
    # ===== FILE HANDLER =====
    if file_output:
        # Tạo thư mục logs nếu chưa tồn tại
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sử dụng RotatingFileHandler để tự động rotate log files
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        # Sử dụng formatter thông thường cho file (có đầy đủ thông tin)
        file_formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=LOG_DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
    
    # Không propagate lên parent logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = 'WeatherApp') -> logging.Logger:
    """
    Lấy logger hiện có hoặc tạo mới nếu chưa tồn tại.
    
    Args:
        name: Tên logger (thường là tên module)
        
    Returns:
        logging.Logger: Logger instance
        
    Example:
        >>> from src.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info('Hello')
    """
    global _app_logger
    
    if _app_logger is None:
        _app_logger = setup_logger(name)
    
    return _app_logger


def log_success(message: str, logger: logging.Logger = None) -> None:
    """
    Log thông báo thành công với emoji.
    
    Args:
        message: Nội dung thông báo
        logger: Logger instance (nếu None sẽ dùng logger mặc định)
    """
    if logger is None:
        logger = get_logger()
    logger.info(f"{EMOJI_SUCCESS} {message}")


def log_error(message: str, logger: logging.Logger = None, exc_info: bool = False) -> None:
    """
    Log thông báo lỗi với emoji.
    
    Args:
        message: Nội dung lỗi
        logger: Logger instance (nếu None sẽ dùng logger mặc định)
        exc_info: Có ghi exception traceback không
    """
    if logger is None:
        logger = get_logger()
    logger.error(f"{EMOJI_ERROR} {message}", exc_info=exc_info)


def log_warning(message: str, logger: logging.Logger = None) -> None:
    """
    Log cảnh báo với emoji.
    
    Args:
        message: Nội dung cảnh báo
        logger: Logger instance (nếu None sẽ dùng logger mặc định)
    """
    if logger is None:
        logger = get_logger()
    logger.warning(f"{EMOJI_WARNING} {message}")


def log_info(message: str, logger: logging.Logger = None) -> None:
    """
    Log thông tin với emoji.
    
    Args:
        message: Nội dung thông tin
        logger: Logger instance (nếu None sẽ dùng logger mặc định)
    """
    if logger is None:
        logger = get_logger()
    logger.info(f"{EMOJI_INFO} {message}")


# Khởi tạo logger mặc định khi module được import
_app_logger = setup_logger()
