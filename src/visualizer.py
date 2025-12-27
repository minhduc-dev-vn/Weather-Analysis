# src/visualizer.py
"""
Module vẽ biểu đồ và trực quan hóa dữ liệu thời tiết.

Chức năng:
    - Vẽ biểu đồ kết hợp (Nhiệt độ + Độ ẩm)
    - Vẽ histogram phân bố nhiệt độ
    - Vẽ biểu đồ tốc gió

Author: Weather Forecast Pro Team
Date: 2025-12-27 (Refactored for code quality)
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend không tương tác
import matplotlib.pyplot as plt
import os
import numpy as np
from typing import Optional
from matplotlib.patches import Patch

from .config import DEFAULT_CITY_VIET, get_processed_data_path, get_chart_path
from .constants import (
    DEFAULT_FIGSIZE, SMALL_FIGSIZE, DEFAULT_DPI,
    COLOR_TEMPERATURE, COLOR_HUMIDITY, COLOR_WIND, COLOR_GAUSSIAN, COLOR_GRID,
    HISTOGRAM_BINS, HISTOGRAM_ALPHA,
    MAX_TIME_POINTS_DISPLAY,
    LINE_WIDTH_DEFAULT, LINE_WIDTH_THICK, FONT_SIZE_TICK, FONT_SIZE_LEGEND
)
from .column_names import CleanColumns
from .exceptions import FileOperationError, ChartGenerationError, EmptyDataFrameError
from .logger import get_logger, log_success, log_error, log_warning, log_info
from .plot_helpers import (
    create_figure, format_plot_labels, format_secondary_axis_labels,
    save_plot_with_config, rotate_xlabels, add_legend, setup_tight_layout
)


# Logger cho module này
logger = get_logger(__name__)


def _load_processed_data(filepath: str) -> pd.DataFrame:
    """
    Đọc dữ liệu đã processed và chuyển đổi thời gian.
    
    Args:
        filepath: Đường dẫn file processed data
        
    Returns:
        pd.DataFrame: DataFrame với thời gian đã converted
        
    Raises:
        FileOperationError: Nếu file không tồn tại hoặc không đọc được
        EmptyDataFrameError: Nếu DataFrame rỗng
    """
    if not os.path.exists(filepath):
        error_msg = f"Chưa có dữ liệu sạch. Vui lòng cập nhật dữ liệu từ API trước"
        log_error(error_msg, logger)
        raise FileOperationError(error_msg, filepath)
    
    try:
        df = pd.read_csv(filepath)
        
        if len(df) == 0:
            error_msg = "Dữ liệu trống"
            log_error(error_msg, logger)
            raise EmptyDataFrameError(error_msg)
        
        df[CleanColumns.THOI_GIAN.value] = pd.to_datetime(df[CleanColumns.THOI_GIAN.value])
        return df
        
    except pd.errors.ParserError as e:
        error_msg = f"Lỗi parse CSV: {e}"
        log_error(error_msg, logger)
        raise FileOperationError(error_msg, filepath) from e


def _validate_column_exists(df: pd.DataFrame, column: str) -> None:
    """
    Kiểm tra cột tồn tại trong DataFrame.
    
    Args:
        df: DataFrame cần kiểm tra
        column: Tên cột cần kiểm tra
        
    Raises:
        ChartGenerationError: Nếu cột không tồn tại
    """
    if column not in df.columns:
        error_msg = f"Không tìm thấy cột '{column}'. Các cột hiện có: {df.columns.tolist()}"
        log_error(error_msg, logger)
        raise ChartGenerationError(error_msg)


def create_weather_chart(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[str]:
    """
    Vẽ biểu đồ kết hợp (Nhiệt độ & Độ ẩm) và lưu thành ảnh PNG.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
        
    Note:
        - Hiển thị 12 mốc thời gian đầu tiên (48 giờ)
        - Sử dụng 2 trục Y để so sánh hai đại lượng
    """
    
    processed_data_path = get_processed_data_path(city_name_viet)
    chart_path = get_chart_path(city_name_viet, "main")
    
    logger.info(f"📊 Đang vẽ biểu đồ thời tiết (Nhiệt độ & Độ ẩm) cho {city_name_viet}...")
    
    try:
        # Load data
        df = _load_processed_data(processed_data_path)
        
        # Validate columns
        _validate_column_exists(df, CleanColumns.NHIET_DO.value)
        _validate_column_exists(df, CleanColumns.DO_AM.value)
        
        # Lấy dữ liệu để plot
        df_plot = df.head(MAX_TIME_POINTS_DISPLAY)
        
        # Tạo figure với background màu
        fig, ax1 = create_figure(figsize=DEFAULT_FIGSIZE)
        fig.patch.set_facecolor('#FAFAFA')  # Background xám rất nhạt
        ax1.set_facecolor('#FFFFFF')  # Plot area trắng
        
        # Trục 1: Nhiệt độ (đường với shadow)
        # Vẽ shadow trước
        ax1.plot(
            df_plot[CleanColumns.THOI_GIAN.value],
            df_plot[CleanColumns.NHIET_DO.value],
            color='#CCCCCC',
            linewidth=LINE_WIDTH_DEFAULT + 1.5,
            alpha=0.3,
            zorder=1
        )
        
        # Vẽ line chính
        line1 = ax1.plot(
            df_plot[CleanColumns.THOI_GIAN.value],
            df_plot[CleanColumns.NHIET_DO.value],
            color=COLOR_TEMPERATURE,
            marker='o',
            linewidth=LINE_WIDTH_DEFAULT,
            markersize=8,
            markerfacecolor=COLOR_TEMPERATURE,
            markeredgecolor='white',
            markeredgewidth=2,
            label='🌡️ Nhiệt Độ',
            zorder=3,
            linestyle='-',
            antialiased=True
        )
        
        # Fill area dưới đường nhiệt độ
        ax1.fill_between(
            df_plot[CleanColumns.THOI_GIAN.value],
            df_plot[CleanColumns.NHIET_DO.value],
            alpha=0.1,
            color=COLOR_TEMPERATURE,
            zorder=1
        )
        
        ax1.tick_params(axis='y', labelcolor=COLOR_TEMPERATURE, labelsize=FONT_SIZE_TICK)
        ax1.spines['left'].set_color(COLOR_TEMPERATURE)
        ax1.spines['left'].set_linewidth(2)
        
        # Trục 2: Độ ẩm (cột với gradient effect)
        ax2 = ax1.twinx()
        bars = ax2.bar(
            df_plot[CleanColumns.THOI_GIAN.value],
            df_plot[CleanColumns.DO_AM.value],
            color=COLOR_HUMIDITY,
            alpha=0.5,
            width=0.02,  # Giảm từ 0.08 để không che khuất đường nhiệt độ
            label='💧 Độ Ẩm',
            edgecolor='white',
            linewidth=0.5,
            zorder=2
        )
        
        # Gradient effect cho bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            bar.set_facecolor(COLOR_HUMIDITY)
            bar.set_alpha(0.5 + (height / df_plot[CleanColumns.DO_AM.value].max()) * 0.3)
        
        ax2.tick_params(axis='y', labelcolor=COLOR_HUMIDITY, labelsize=FONT_SIZE_TICK)
        ax2.spines['right'].set_color(COLOR_HUMIDITY)
        ax2.spines['right'].set_linewidth(2)
        
        # Format labels với style đẹp hơn
        format_plot_labels(
            ax1,
            title=f'📊 Dự báo Thời tiết: Nhiệt độ & Độ ẩm (48 giờ)\n{city_name_viet}',
            xlabel='⏰ Thời Gian (Dự báo 3h/lần)',
            ylabel='🌡️ Nhiệt Độ (°C)',
            enable_grid=True
        )
        
        format_secondary_axis_labels(
            ax2,
            ylabel='💧 Độ Ẩm (%)'
        )
        
        # Grid đẹp hơn
        ax1.grid(True, alpha=0.2, linestyle=':', linewidth=1, color=COLOR_GRID, zorder=0)
        ax1.set_axisbelow(True)
        
        # Xoay labels và tạo spacing tốt hơn
        rotate_xlabels(ax1, rotation=30)
        
        # Legend đẹp hơn với shadow
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        legend = ax1.legend(
            lines1 + lines2, 
            labels1 + labels2, 
            loc='upper left',
            fontsize=FONT_SIZE_LEGEND,
            framealpha=0.95,
            edgecolor='#DDDDDD',
            fancybox=True,
            shadow=True
        )
        
        # Border đẹp hơn
        for spine in ax1.spines.values():
            if spine not in [ax1.spines['left']]:
                spine.set_linewidth(1.5)
                spine.set_color('#DDDDDD')
        
        # Lưu file với DPI cao hơn
        setup_tight_layout(fig)
        save_plot_with_config(fig, chart_path, dpi=DEFAULT_DPI)
        
        return chart_path
        
    except (FileOperationError, ChartGenerationError, EmptyDataFrameError) as e:
        logger.error(f"Lỗi khi vẽ biểu đồ: {e}")
        plt.close('all')
        return None
        
    except Exception as e:
        log_error(f"Lỗi không xác định khi vẽ biểu đồ: {e}", logger, exc_info=True)
        plt.close('all')
        return None


def create_temperature_histogram(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[str]:
    """
    Vẽ histogram phân bố nhiệt độ và lưu thành ảnh.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
        
    Note:
        - Hiển thị phân bố dữ liệu nhiệt độ
        - Có đường cong Gaussian overlay
    """
    
    processed_data_path = get_processed_data_path(city_name_viet)
    chart_path = get_chart_path(city_name_viet, "histogram")
    
    logger.info(f"📊 Đang vẽ histogram phân bố nhiệt độ cho {city_name_viet}...")
    
    try:
        # Load data
        df = _load_processed_data(processed_data_path)
        _validate_column_exists(df, CleanColumns.NHIET_DO.value)
        
        # Tạo figure
        fig, ax = create_figure(figsize=SMALL_FIGSIZE)
        
        # Vẽ histogram
        n, bins, patches = ax.hist(
            df[CleanColumns.NHIET_DO.value],
            bins=HISTOGRAM_BINS,
            color=COLOR_TEMPERATURE,
            alpha=HISTOGRAM_ALPHA,
            edgecolor='black',
            linewidth=1.5
        )
        
        # Thêm đường cong Gaussian
        mu = df[CleanColumns.NHIET_DO.value].mean()
        sigma = df[CleanColumns.NHIET_DO.value].std()
        x = np.linspace(
            df[CleanColumns.NHIET_DO.value].min(),
            df[CleanColumns.NHIET_DO.value].max(),
            100
        )
        gaussian = (
            len(df) * (bins[1] - bins[0]) / np.sqrt(2 * np.pi * sigma**2) *
            np.exp(-(x - mu)**2 / (2 * sigma**2))
        )
        ax.plot(x, gaussian, color=COLOR_GAUSSIAN, linewidth=LINE_WIDTH_DEFAULT, label='Đường Gaussian')
        
        # Format labels
        format_plot_labels(
            ax,
            title=f'📈 Phân bố Nhiệt độ - {city_name_viet}',
            xlabel='Nhiệt Độ (°C)',
            ylabel='Số lần xuất hiện'
        )
        
        # Thêm thống kê
        stats_text = f'μ = {mu:.1f}°C\nσ = {sigma:.1f}°C'
        ax.text(
            0.98, 0.97, stats_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        add_legend(ax)
        
        # Lưu file
        setup_tight_layout(fig)
        save_plot_with_config(fig, chart_path, dpi=DEFAULT_DPI)
        
        return chart_path
        
    except (FileOperationError, ChartGenerationError, EmptyDataFrameError) as e:
        logger.error(f"Lỗi khi vẽ histogram: {e}")
        plt.close('all')
        return None
        
    except Exception as e:
        log_error(f"Lỗi không xác định khi vẽ histogram: {e}", logger, exc_info=True)
        plt.close('all')
        return None


def create_wind_speed_chart(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[str]:
    """
    Vẽ biểu đồ tốc gió và lưu thành ảnh.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    processed_data_path = get_processed_data_path(city_name_viet)
    chart_path = get_chart_path(city_name_viet, "wind")
    
    logger.info(f"📊 Đang vẽ biểu đồ tốc gió cho {city_name_viet}...")
    
    try:
        # Load data
        df = _load_processed_data(processed_data_path)
        _validate_column_exists(df, CleanColumns.TOC_GIO.value)
        
        df_plot = df.head(MAX_TIME_POINTS_DISPLAY)
        
        # Tạo figure
        fig, ax = create_figure(figsize=DEFAULT_FIGSIZE)
        
        # Vẽ biểu đồ cột
        bars = ax.bar(
            range(len(df_plot)),
            df_plot[CleanColumns.TOC_GIO.value],
            color=COLOR_WIND,
            alpha=HISTOGRAM_ALPHA,
            edgecolor='black',
            linewidth=1.5
        )
        
        # Tô màu dựa trên cường độ gió
        colors = [
            'darkgreen' if x >= 10 else 'orange' if x >= 5 else 'lightgreen'
            for x in df_plot[CleanColumns.TOC_GIO.value]
        ]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # Format labels
        format_plot_labels(
            ax,
            title=f'💨 Dự báo Tốc Gió (48h) - {city_name_viet}',
            xlabel='Thời Gian (Dự báo 3h/lần)',
            ylabel='Tốc Gió (m/s)'
        )
        
        # Set x-tick labels
        ax.set_xticks(range(len(df_plot)))
        ax.set_xticklabels(
            [t.strftime('%m/%d %H:%M') for t in df_plot[CleanColumns.THOI_GIAN.value]],
            rotation=45,
            ha='right'
        )
        
        # Thêm legend cho mức độ gió
        legend_elements = [
            Patch(facecolor='darkgreen', label='Rất mạnh (≥10 m/s)'),
            Patch(facecolor='orange', label='Mạnh (5-10 m/s)'),
            Patch(facecolor='lightgreen', label='Nhẹ (<5 m/s)')
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        
        # Lưu file
        setup_tight_layout(fig)
        save_plot_with_config(fig, chart_path, dpi=DEFAULT_DPI)
        
        return chart_path
        
    except (FileOperationError, ChartGenerationError, EmptyDataFrameError) as e:
        logger.error(f"Lỗi khi vẽ biểu đồ tốc gió: {e}")
        plt.close('all')
        return None
        
    except Exception as e:
        log_error(f"Lỗi không xác định khi vẽ biểu đồ tốc gió: {e}", logger, exc_info=True)
        plt.close('all')
        return None


def create_all_charts(city_name_viet: str = DEFAULT_CITY_VIET) -> bool:
    """
    Vẽ tất cả các biểu đồ (kết hợp, histogram, tốc gió).
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        bool: True nếu vẽ thành công tất cả, False nếu có biểu đồ thất bại
    """
    
    logger.info("\n" + "="*50)
    logger.info(f"🎨 TRỰC QUAN HÓA DỮ LIỆU THỜI TIẾT - {city_name_viet}")
    logger.info("="*50 + "\n")
    
    results = {
        'Biểu đồ chính': create_weather_chart(city_name_viet),
        'Histogram': create_temperature_histogram(city_name_viet),
        'Tốc gió': create_wind_speed_chart(city_name_viet)
    }
    
    logger.info("\n" + "="*50)
    logger.info("📊 KẾT QUẢ VẼ BIỂU ĐỒ:")
    logger.info("="*50)
    for name, path in results.items():
        status = "✅ Thành công" if path else "❌ Thất bại"
        logger.info(f"{name:20} {status}")
    
    success = all(v is not None for v in results.values())
    if success:
        log_success("Tất cả biểu đồ đã được tạo thành công", logger)
    else:
        log_warning("Một số biểu đồ tạo thất bại", logger)
    
    return success


if __name__ == "__main__":
    create_all_charts()