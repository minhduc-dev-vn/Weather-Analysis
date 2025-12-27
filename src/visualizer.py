# src/visualizer.py
"""
Module vẽ biểu đồ và trực quan hóa dữ liệu thời tiết.

Chức năng:
    - Vẽ biểu đồ kết hợp (Nhiệt độ + Độ ẩm)
    - Vẽ histogram phân bố nhiệt độ
    - Vẽ biểu đồ tốc gió
    - Tính toán và hiển thị thống kê

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set backend không tương tác để tránh conflict với threading
import matplotlib.pyplot as plt
import os
import numpy as np
from typing import Optional
from .config import DEFAULT_CITY_VIET, get_processed_data_path, get_chart_path


def create_weather_chart(city_name_viet: str = DEFAULT_CITY_VIET) -> Optional[str]:
    """
    Vẽ biểu đồ kết hợp (Nhiệt độ & Độ ẩm) và lưu thành ảnh PNG.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
        
    Raises:
        FileNotFoundError: File dữ liệu sạch không tồn tại
        Exception: Các lỗi khác
        
    Note:
        - Hiển thị 12 mốc thời gian đầu tiên (48 giờ)
        - Sử dụng 2 trục Y để so sánh hai đại lượng
    """
    
    processed_data_path = get_processed_data_path(city_name_viet)
    chart_path = get_chart_path(city_name_viet, "main")
    
    # ===== KIỂM TRA FILE =====
    if not os.path.exists(processed_data_path):
        print(f"⚠️ Chưa có dữ liệu sạch để vẽ cho {city_name_viet}")
        print("💡 Vui lòng cập nhật dữ liệu từ API trước")
        return None

    print(f"📊 Đang vẽ biểu đồ thời tiết (Nhiệt độ & Độ ẩm) cho {city_name_viet}...")
    
    try:
        # ===== ĐỌC DỮ LIỆU =====
        df = pd.read_csv(processed_data_path)
        
        if len(df) == 0:
            print("❌ LỖI: Dữ liệu trống")
            return None
        
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        df_plot = df.head(12)  # Lấy 12 mốc đầu (48 giờ)
        
        # ===== VẼ BIỂU ĐỒ =====
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # --- Trục 1: Nhiệt độ (Đường màu đỏ) ---
        color_temp = 'tab:red'
        ax1.set_xlabel('Thời Gian (Dự báo 3h/lần)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Nhiệt Độ (°C)', color=color_temp, fontsize=12, fontweight='bold')
        line = ax1.plot(df_plot['Thời Gian'], df_plot['Nhiệt Độ'], 
                       color=color_temp, marker='o', linewidth=2.5, 
                       markersize=6, label='Nhiệt Độ')
        ax1.tick_params(axis='y', labelcolor=color_temp)
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # --- Trục 2: Độ ẩm (Cột màu xanh) ---
        ax2 = ax1.twinx()
        color_hum = 'tab:blue'
        ax2.set_ylabel('Độ Ẩm (%)', color=color_hum, fontsize=12, fontweight='bold')
        bar = ax2.bar(df_plot['Thời Gian'], df_plot['Độ Ẩm'], 
                     color=color_hum, alpha=0.3, width=0.5, label='Độ Ẩm')
        ax2.tick_params(axis='y', labelcolor=color_hum)
        
        # ===== TRANG TRÍ =====
        plt.title(f'📊 Dự báo Thời tiết: Nhiệt độ & Độ ẩm (48 giờ) - {city_name_viet}', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Xoay nhãn trục X để dễ đọc
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Thêm legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
        
        # ===== LƯU FILE =====
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ: {e}")
        plt.close()
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
    
    if not os.path.exists(processed_data_path):
        print(f"⚠️ Chưa có dữ liệu để vẽ histogram cho {city_name_viet}")
        return None

    print(f"📊 Đang vẽ biểu đồ histogram (phân bố nhiệt độ) cho {city_name_viet}...")
    
    try:
        df = pd.read_csv(processed_data_path)
        
        # Validate column
        if 'Nhiệt Độ' not in df.columns:
            print(f"❌ Không tìm thấy cột 'Nhiệt Độ'")
            print(f"   Các cột có sẵn: {df.columns.tolist()}")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # ===== VẼ HISTOGRAM =====
        n, bins, patches = ax.hist(df['Nhiệt Độ'], bins=10, color='tab:red', 
                                    alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # ===== THÊM ĐƯỜNG CONG GAUSSIAN =====
        mu, sigma = df['Nhiệt Độ'].mean(), df['Nhiệt Độ'].std()
        x = np.linspace(df['Nhiệt Độ'].min(), df['Nhiệt Độ'].max(), 100)
        gaussian = (len(df) * (bins[1] - bins[0]) / np.sqrt(2 * np.pi * sigma**2) * 
                   np.exp(-(x - mu)**2 / (2 * sigma**2)))
        ax.plot(x, gaussian, 'b-', linewidth=2.5, label='Đường Gaussian')
        
        # ===== TRANG TRÍ =====
        ax.set_xlabel('Nhiệt Độ (°C)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Số lần xuất hiện', fontsize=12, fontweight='bold')
        ax.set_title(f'📈 Phân bố Nhiệt độ - {city_name_viet}', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # ===== THÊM THỐNG KÊ =====
        stats_text = f'μ = {mu:.1f}°C\nσ = {sigma:.1f}°C'
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, 
               fontsize=11, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.legend(fontsize=10)
        
        # ===== LƯU FILE =====
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu histogram: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ histogram: {e}")
        plt.close()
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
    
    if not os.path.exists(processed_data_path):
        print(f"⚠️ Chưa có dữ liệu để vẽ biểu đồ tốc gió cho {city_name_viet}")
        return None

    print(f"📊 Đang vẽ biểu đồ tốc gió cho {city_name_viet}...")
    
    try:
        df = pd.read_csv(processed_data_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        
        # Validate column
        if 'Tốc Gió' not in df.columns:
            print(f"❌ Không tìm thấy cột 'Tốc Gió'")
            print(f"   Các cột có sẵn: {df.columns.tolist()}")
            return None
        
        df_plot = df.head(12)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # ===== VẼ BIỂU ĐỒ CỘT =====
        bars = ax.bar(range(len(df_plot)), df_plot['Tốc Gió'], 
                      color='tab:green', alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # ===== TÍNH THỨ TỰ GIÓ =====
        # Tô màu các thanh dựa trên cường độ
        colors = ['darkgreen' if x >= 10 else 'orange' if x >= 5 else 'lightgreen' 
                 for x in df_plot['Tốc Gió']]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # ===== TRANG TRÍ =====
        ax.set_xlabel('Thời Gian (Dự báo 3h/lần)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tốc Gió (m/s)', fontsize=12, fontweight='bold')
        ax.set_title(f'💨 Dự báo Tốc Gió (48 giờ) - {city_name_viet}', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(len(df_plot)))
        ax.set_xticklabels([t.strftime('%m/%d %H:%M') for t in df_plot['Thời Gian']], 
                           rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # ===== THÊM LEGEND =====
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='darkgreen', label='Rất mạnh (≥10 m/s)'),
            Patch(facecolor='orange', label='Mạnh (5-10 m/s)'),
            Patch(facecolor='lightgreen', label='Nhẹ (<5 m/s)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        # ===== LƯU FILE =====
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ tốc gió: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ tốc gió: {e}")
        plt.close()
        return None


def create_all_charts(city_name_viet: str = DEFAULT_CITY_VIET) -> bool:
    """
    Vẽ tất cả các biểu đồ (kết hợp, histogram, tốc gió).
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt (mặc định: "Hà Nội")
    
    Returns:
        bool: True nếu vẽ thành công, False nếu thất bại
    """
    
    print("\n" + "="*50)
    print(f"🎨 TRỰC QUAN HÓA DỮ LIỆU THỜI TIẾT - {city_name_viet}")
    print("="*50 + "\n")
    
    results = {
        'Biểu đồ chính': create_weather_chart(city_name_viet),
        'Histogram': create_temperature_histogram(city_name_viet),
        'Tốc gió': create_wind_speed_chart(city_name_viet)
    }
    
    print("\n" + "="*50)
    print("📊 KẾT QUẢ VẼ BIỂU ĐỒ:")
    print("="*50)
    for name, path in results.items():
        status = "✅ Thành công" if path else "❌ Thất bại"
        print(f"{name:20} {status}")
    
    return all(v is not None for v in results.values())


if __name__ == "__main__":
    create_all_charts()