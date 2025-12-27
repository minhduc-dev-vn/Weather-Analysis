# src/plot_helpers.py
"""
Module chứa các hàm helper cho việc vẽ biểu đồ.

Mục đích:
    - Loại bỏ duplicate code trong visualizer.py và visualizer_advanced.py
    - Tập trung cấu hình matplotlib vào một nơi
    - Đảm bảo tính nhất quán giữa các biểu đồ

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import Optional, Tuple
import os

from .constants import (
    DEFAULT_FIGSIZE, DEFAULT_DPI,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_LABEL, FONT_SIZE_TICK,
    FONT_WEIGHT_BOLD, FONT_WEIGHT_NORMAL,
    GRID_ALPHA, GRID_LINESTYLE
)
from .logger import get_logger, log_success, log_error
from .exceptions import ChartGenerationError


# Logger cho module này
logger = get_logger(__name__)


def setup_vietnamese_font() -> None:
    """
    Cấu hình font để hiển thị tiếng Việt.
    
    Note:
        - Matplotlib mặc định không hỗ trợ Unicode tốt
        - Hàm này thiết lập font có hỗ trợ tiếng Việt
    """
    try:
        # Thiết lập font mặc định
        matplotlib.rcParams['font.family'] = FONT_FAMILY
        matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False  # Hiển thị dấu trừ đúng
        
        logger.debug("Đã cấu hình font tiếng Việt")
    except Exception as e:
        log_error(f"Không thể cấu hình font: {e}", logger)


def setup_plot_style() -> None:
    """
    Thiết lập style mặc định cho tất cả các biểu đồ.
    
    Note:
        - Gọi hàm này một lần khi khởi động ứng dụng
        - Hoặc gọi trước khi vẽ biểu đồ để reset style
    """
    try:
        # Font
        setup_vietnamese_font()
        
        # Grid
        matplotlib.rcParams['axes.grid'] = True
        matplotlib.rcParams['grid.alpha'] = GRID_ALPHA
        matplotlib.rcParams['grid.linestyle'] = GRID_LINESTYLE
        
        # Figure
        matplotlib.rcParams['figure.dpi'] = DEFAULT_DPI
        matplotlib.rcParams['savefig.dpi'] = DEFAULT_DPI
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        
        logger.debug("Đã thiết lập plot style")
    except Exception as e:
        log_error(f"Không thể thiết lập plot style: {e}", logger)


def create_figure(
    figsize: Optional[Tuple[int, int]] = None,
    dpi: Optional[int] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Tạo figure và axes với kích thước chuẩn.
    
    Args:
        figsize: Kích thước figure (width, height). Nếu None dùng DEFAULT_FIGSIZE
        dpi: DPI của figure. Nếu None dùng DEFAULT_DPI
        
    Returns:
        Tuple[plt.Figure, plt.Axes]: Figure và axes đã tạo
        
    Example:
        >>> fig, ax = create_figure()
        >>> ax.plot([1, 2, 3])
    """
    if figsize is None:
        figsize = DEFAULT_FIGSIZE
    if dpi is None:
        dpi = DEFAULT_DPI
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    return fig, ax


def format_plot_labels(
    ax: plt.Axes,
    title: str,
    xlabel: str,
    ylabel: str,
    title_fontsize: Optional[int] = None,
    label_fontsize: Optional[int] = None,
    title_weight: str = FONT_WEIGHT_BOLD,
    enable_grid: bool = True
) -> None:
    """
    Định dạng labels và title cho biểu đồ.
    
    Args:
        ax: Matplotlib axes object
        title: Tiêu đề biểu đồ
        xlabel: Nhãn trục X
        ylabel: Nhãn trục Y
        title_fontsize: Kích thước font tiêu đề (mặc định: FONT_SIZE_TITLE)
        label_fontsize: Kích thước font nhãn (mặc định: FONT_SIZE_LABEL)
        title_weight: Font weight cho tiêu đề
        enable_grid: Có hiển thị grid không
        
    Example:
        >>> fig, ax = create_figure()
        >>> ax.plot(data)
        >>> format_plot_labels(ax, 'Nhiệt độ', 'Thời gian', 'Độ C')
    """
    if title_fontsize is None:
        title_fontsize = FONT_SIZE_TITLE
    if label_fontsize is None:
        label_fontsize = FONT_SIZE_LABEL
    
    # Title
    ax.set_title(
        title,
        fontsize=title_fontsize,
        fontweight=title_weight,
        fontname=FONT_FAMILY,
        pad=15
    )
    
    # Labels
    ax.set_xlabel(
        xlabel,
        fontsize=label_fontsize,
        fontweight=FONT_WEIGHT_NORMAL,
        fontname=FONT_FAMILY
    )
    ax.set_ylabel(
        ylabel,
        fontsize=label_fontsize,
        fontweight=FONT_WEIGHT_NORMAL,
        fontname=FONT_FAMILY
    )
    
    # Tick labels
    ax.tick_params(axis='both', labelsize=FONT_SIZE_TICK)
    
    # Grid
    if enable_grid:
        ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)


def format_secondary_axis_labels(
    ax: plt.Axes,
    ylabel: str,
    label_fontsize: Optional[int] = None
) -> None:
    """
    Định dạng labels cho trục Y phụ (secondary axis).
    
    Args:
        ax: Matplotlib axes object (thường là ax2 = ax1.twinx())
        ylabel: Nhãn trục Y phụ
        label_fontsize: Kích thước font nhãn
    """
    if label_fontsize is None:
        label_fontsize = FONT_SIZE_LABEL
    
    ax.set_ylabel(
        ylabel,
        fontsize=label_fontsize,
        fontweight=FONT_WEIGHT_NORMAL,
        fontname=FONT_FAMILY
    )
    ax.tick_params(axis='y', labelsize=FONT_SIZE_TICK)


def save_plot_with_config(
    fig: plt.Figure,
    filepath: str,
    dpi: Optional[int] = None,
    close_after_save: bool = True
) -> bool:
    """
    Lưu biểu đồ với cấu hình chuẩn và xử lý lỗi.
    
    Args:
        fig: Figure cần lưu
        filepath: Đường dẫn file output
        dpi: DPI khi lưu (mặc định: DEFAULT_DPI)
        close_after_save: Có đóng figure sau khi lưu không
        
    Returns:
        bool: True nếu lưu thành công, False nếu thất bại
        
    Raises:
        ChartGenerationError: Nếu không thể lưu file
        
    Example:
        >>> fig, ax = create_figure()
        >>> ax.plot([1, 2, 3])
        >>> success = save_plot_with_config(fig, 'chart.png')
    """
    if dpi is None:
        dpi = DEFAULT_DPI
    
    try:
        # Tạo thư mục nếu chưa tồn tại
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Lưu file
        fig.savefig(
            filepath,
            dpi=dpi,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )
        
        # Đóng figure để giải phóng memory
        if close_after_save:
            plt.close(fig)
        
        # Kiểm tra file đã được tạo
        if not os.path.exists(filepath):
            raise ChartGenerationError(
                f"File không được tạo sau khi lưu: {filepath}"
            )
        
        file_size = os.path.getsize(filepath)
        log_success(
            f"Đã lưu biểu đồ: {filepath} ({file_size / 1024:.1f} KB)",
            logger
        )
        return True
        
    except PermissionError as e:
        error_msg = f"Không có quyền ghi file: {filepath}"
        log_error(error_msg, logger, exc_info=True)
        raise ChartGenerationError(error_msg) from e
        
    except OSError as e:
        error_msg = f"Lỗi I/O khi lưu file: {filepath} - {e}"
        log_error(error_msg, logger, exc_info=True)
        raise ChartGenerationError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Lỗi không xác định khi lưu biểu đồ: {e}"
        log_error(error_msg, logger, exc_info=True)
        raise ChartGenerationError(error_msg) from e


def rotate_xlabels(
    ax: plt.Axes,
    rotation: int = 45,
    ha: str = 'right'
) -> None:
    """
    Xoay labels trục X để tránh chồng chéo.
    
    Args:
        ax: Matplotlib axes object
        rotation: Góc xoay (độ)
        ha: Horizontal alignment ('left', 'center', 'right')
    """
    ax.tick_params(axis='x', rotation=rotation)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotation, ha=ha)


def add_legend(
    ax: plt.Axes,
    loc: str = 'best',
    fontsize: Optional[int] = None,
    framealpha: float = 0.9
) -> None:
    """
    Thêm legend với style chuẩn.
    
    Args:
        ax: Matplotlib axes object
        loc: Vị trí legend ('best', 'upper left', 'upper right', etc.)
        fontsize: Kích thước font
        framealpha: Độ trong suốt của frame
    """
    if fontsize is None:
        fontsize = FONT_SIZE_TICK
    
    ax.legend(
        loc=loc,
        fontsize=fontsize,
        framealpha=framealpha,
        edgecolor='gray'
    )


def setup_tight_layout(fig: plt.Figure) -> None:
    """
    Áp dụng tight_layout để tránh chồng chéo.
    
    Args:
        fig: Figure cần adjust
    """
    try:
        fig.tight_layout()
    except Exception as e:
        logger.warning(f"Không thể áp dụng tight_layout: {e}")


# Khởi tạo plot style khi module được import
setup_plot_style()
