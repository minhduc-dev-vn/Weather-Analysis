# src/visualizer_advanced.py
"""
Module vẽ biểu đồ nâng cao và trực quan hóa dữ liệu thời tiết.

Chức năng:
    - So sánh nhiều thành phố
    - Heatmap tương quan
    - Boxplot phân bố
    - Radar chart đa chiều
    - Biểu đồ áp suất và tầm nhìn
    - Biểu đồ hướng gió (wind rose)

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set backend không tương tác để tránh conflict với threading
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import seaborn as sns
from typing import Optional, List, Dict
from .config import get_processed_data_path, get_chart_path, MULTI_CITY_CHART_PATH, VIETNAM_CITIES


def create_comparison_chart(city_list: List[str], metric: str = 'Nhiệt Độ') -> Optional[str]:
    """
    Vẽ biểu đồ so sánh một metric giữa nhiều thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
        metric: Metric cần so sánh (Nhiệt Độ, Độ Ẩm, Tốc Gió, ...)
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ biểu đồ so sánh {metric} giữa các thành phố...")
    
    try:
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Đọc dữ liệu từ các thành phố
        all_data = []
        colors = plt.cm.Set3(np.linspace(0, 1, len(city_list)))
        
        for idx, city in enumerate(city_list):
            processed_path = get_processed_data_path(city)
            if not os.path.exists(processed_path):
                print(f"⚠️ Không tìm thấy dữ liệu cho {city}")
                continue
            
            df = pd.read_csv(processed_path)
            df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
            
            # Validate column exists
            if metric not in df.columns:
                print(f"⚠️ Không tìm thấy cột '{metric}' trong dữ liệu {city}")
                print(f"   Các cột có sẵn: {df.columns.tolist()}")
                continue
            
            # Vẽ đường cho từng thành phố
            ax.plot(df['Thời Gian'], df[metric], 
                   marker='o', linewidth=2, markersize=4,
                   label=city, color=colors[idx], alpha=0.8)
            
            all_data.append(df[metric].values)
        
        ax.set_xlabel('Thời Gian', fontsize=12, fontweight='bold')
        ax.set_ylabel(metric, fontsize=12, fontweight='bold')
        ax.set_title(f'📊 So Sánh {metric} Giữa Các Thành Phố', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Lưu file
        chart_path = MULTI_CITY_CHART_PATH.replace('.png', f'_comparison_{metric.replace(" ", "_")}.png')
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ so sánh: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ so sánh: {e}")
        plt.close()
        return None


def create_correlation_heatmap(city_name_viet: str = "Hà Nội") -> Optional[str]:
    """
    Vẽ heatmap tương quan giữa các biến số.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ heatmap tương quan cho {city_name_viet}...")
    
    try:
        processed_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_path):
            print(f"⚠️ Không tìm thấy dữ liệu cho {city_name_viet}")
            return None
        
        df = pd.read_csv(processed_path)
        
        # Chọn các cột số và kiểm tra tồn tại
        numeric_cols = ['Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió']
        if 'Nhiệt Độ Cảm Nhận' in df.columns:
            numeric_cols.append('Nhiệt Độ Cảm Nhận')
        if 'Độ Che Phủ Mây' in df.columns:
            numeric_cols.append('Độ Che Phủ Mây')
        if 'Tầm Nhìn' in df.columns:
            numeric_cols.append('Tầm Nhìn')
        
        # Lọc ra các cột thực sự tồn tại trong DataFrame
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        if len(numeric_cols) < 2:
            print(f"❌ Không đủ cột số để tạo heatmap (cần ít nhất 2 cột)")
            return None
        
        # Tính ma trận tương quan
        corr_matrix = df[numeric_cols].corr()
        
        # Vẽ heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax, vmin=-1, vmax=1)
        
        ax.set_title(f'🔥 Heatmap Tương Quan Các Biến - {city_name_viet}',
                    fontsize=14, fontweight='bold', pad=20)
        
        # Lưu file
        chart_path = get_chart_path(city_name_viet, "heatmap")
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu heatmap: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ heatmap: {e}")
        plt.close()
        return None


def create_boxplot(city_list: List[str], metric: str = 'Nhiệt Độ') -> Optional[str]:
    """
    Vẽ boxplot so sánh phân bố một metric giữa các thành phố.
    
    Args:
        city_list: Danh sách tên thành phố tiếng Việt
        metric: Metric cần so sánh
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ boxplot {metric} cho các thành phố...")
    
    try:
        data_to_plot = []
        labels = []
        
        for city in city_list:
            processed_path = get_processed_data_path(city)
            if not os.path.exists(processed_path):
                continue
            
            df = pd.read_csv(processed_path)
            
            # Validate column exists
            if metric not in df.columns:
                print(f"⚠️ '{metric}' không tồn tại trong dữ liệu {city}")
                continue
            
            data_to_plot.append(df[metric].values)
            labels.append(city)
        
        if len(data_to_plot) == 0:
            print("❌ Không có dữ liệu để vẽ")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True, 
                       showmeans=True, meanline=True)
        
        # Tô màu các box
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(bp['boxes'])))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel(metric, fontsize=12, fontweight='bold')
        ax.set_title(f'📦 Phân Bố {metric} Giữa Các Thành Phố',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.xticks(rotation=45, ha='right')
        
        # Lưu file
        chart_path = MULTI_CITY_CHART_PATH.replace('.png', f'_boxplot_{metric.replace(" ", "_")}.png')
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu boxplot: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ boxplot: {e}")
        plt.close()
        return None


def create_pressure_chart(city_name_viet: str = "Hà Nội") -> Optional[str]:
    """
    Vẽ biểu đồ Áp suất riêng biệt.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ biểu đồ Áp suất cho {city_name_viet}...")
    
    try:
        processed_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_path):
            print(f"⚠️ Không tìm thấy dữ liệu cho {city_name_viet}")
            return None
        
        df = pd.read_csv(processed_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        
        if 'Áp Suất' not in df.columns:
            print("⚠️ Không có dữ liệu Áp Suất")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Vẽ đường áp suất
        ax.plot(df['Thời Gian'], df['Áp Suất'], 
                color='tab:blue', marker='o', linewidth=2.5, 
                markersize=6, label='Áp Suất')
        ax.fill_between(df['Thời Gian'], df['Áp Suất'], alpha=0.3, color='tab:blue')
        
        # Thêm đường trung bình
        mean_pressure = df['Áp Suất'].mean()
        ax.axhline(y=mean_pressure, color='red', linestyle='--', 
                   alpha=0.7, label=f'Trung bình: {mean_pressure:.0f} hPa')
        
        ax.set_xlabel('Thời Gian', fontsize=12, fontweight='bold')
        ax.set_ylabel('Áp Suất (hPa)', fontsize=12, fontweight='bold')
        ax.set_title(f'📊 Áp Suất Khí Quyển - {city_name_viet}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='best', fontsize=10)
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Lưu file
        chart_path = get_chart_path(city_name_viet, "pressure")
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ áp suất: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ áp suất: {e}")
        plt.close()
        return None


def create_visibility_chart(city_name_viet: str = "Hà Nội") -> Optional[str]:
    """
    Vẽ biểu đồ Tầm nhìn riêng biệt.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ biểu đồ Tầm nhìn cho {city_name_viet}...")
    
    try:
        processed_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_path):
            print(f"⚠️ Không tìm thấy dữ liệu cho {city_name_viet}")
            return None
        
        df = pd.read_csv(processed_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        
        if 'Tầm Nhìn' not in df.columns:
            print("⚠️ Không có dữ liệu Tầm Nhìn")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Vẽ cột tầm nhìn
        bars = ax.bar(df['Thời Gian'], df['Tầm Nhìn'], 
                      color='tab:orange', alpha=0.7, edgecolor='darkorange', linewidth=1.5)
        
        # Tô màu theo mức độ tầm nhìn
        colors = ['red' if x < 5 else 'orange' if x < 8 else 'green' 
                 for x in df['Tầm Nhìn']]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
            bar.set_alpha(0.7)
        
        ax.set_xlabel('Thời Gian', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tầm Nhìn (km)', fontsize=12, fontweight='bold')
        ax.set_title(f'👁️ Tầm Nhìn - {city_name_viet}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Thêm legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Tốt (≥8 km)'),
            Patch(facecolor='orange', alpha=0.7, label='Trung bình (5-8 km)'),
            Patch(facecolor='red', alpha=0.7, label='Kém (<5 km)')
        ]
        ax.legend(handles=legend_elements, loc='best', fontsize=10)
        
        # Lưu file
        chart_path = get_chart_path(city_name_viet, "visibility")
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ tầm nhìn: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ tầm nhìn: {e}")
        plt.close()
        return None

def create_pressure_visibility_chart(city_name_viet: str = "Hà Nội") -> Optional[str]:
    """
    Vẽ biểu đồ kết hợp Áp suất và Tầm nhìn.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ biểu đồ Áp suất & Tầm nhìn cho {city_name_viet}...")
    
    try:
        processed_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_path):
            print(f"⚠️ Không tìm thấy dữ liệu cho {city_name_viet}")
            return None
        
        df = pd.read_csv(processed_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        
        if 'Áp Suất' not in df.columns:
            print("⚠️ Không có dữ liệu Áp Suất")
            return None
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Trục 1: Áp suất
        color1 = 'tab:blue'
        ax1.set_xlabel('Thời Gian', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Áp Suất (hPa)', color=color1, fontsize=12, fontweight='bold')
        line1 = ax1.plot(df['Thời Gian'], df['Áp Suất'], 
                        color=color1, marker='o', linewidth=2.5, 
                        markersize=6, label='Áp Suất')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # Trục 2: Tầm nhìn (nếu có)
        if 'Tầm Nhìn' in df.columns:
            ax2 = ax1.twinx()
            color2 = 'tab:orange'
            ax2.set_ylabel('Tầm Nhìn (km)', color=color2, fontsize=12, fontweight='bold')
            line2 = ax2.plot(df['Thời Gian'], df['Tầm Nhìn'], 
                           color=color2, marker='s', linewidth=2.5, 
                           markersize=6, label='Tầm Nhìn', linestyle='--')
            ax2.tick_params(axis='y', labelcolor=color2)
        
        plt.title(f'📊 Áp Suất & Tầm Nhìn - {city_name_viet}',
                 fontsize=14, fontweight='bold', pad=20)
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        if 'Tầm Nhìn' in df.columns:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
        else:
            ax1.legend(lines1, labels1, loc='upper left', fontsize=10)
        
        # Lưu file
        chart_path = get_chart_path(city_name_viet, "pressure_visibility")
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ áp suất & tầm nhìn: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ áp suất & tầm nhìn: {e}")
        plt.close()
        return None


def create_cloud_cover_chart(city_name_viet: str = "Hà Nội") -> Optional[str]:
    """
    Vẽ biểu đồ độ che phủ mây.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Optional[str]: Đường dẫn file ảnh nếu thành công, None nếu thất bại
    """
    
    print(f"📊 Đang vẽ biểu đồ độ che phủ mây cho {city_name_viet}...")
    
    try:
        processed_path = get_processed_data_path(city_name_viet)
        if not os.path.exists(processed_path):
            print(f"⚠️ Không tìm thấy dữ liệu cho {city_name_viet}")
            return None
        
        df = pd.read_csv(processed_path)
        df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
        
        if 'Độ Che Phủ Mây' not in df.columns:
            print("⚠️ Không có dữ liệu Độ Che Phủ Mây")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Vẽ biểu đồ vùng với màu gradient
        ax.fill_between(df['Thời Gian'], 0, df['Độ Che Phủ Mây'], 
                        alpha=0.3, color='gray', label='Độ Che Phủ Mây')
        ax.plot(df['Thời Gian'], df['Độ Che Phủ Mây'], 
               marker='o', linewidth=2, markersize=6, color='darkgray')
        
        # Thêm đường phân loại
        ax.axhline(y=25, color='green', linestyle='--', alpha=0.5, label='Trời quang (0-25%)')
        ax.axhline(y=50, color='yellow', linestyle='--', alpha=0.5, label='Ít mây (25-50%)')
        ax.axhline(y=75, color='orange', linestyle='--', alpha=0.5, label='Nhiều mây (50-75%)')
        
        ax.set_xlabel('Thời Gian', fontsize=12, fontweight='bold')
        ax.set_ylabel('Độ Che Phủ Mây (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'☁️ Độ Che Phủ Mây - {city_name_viet}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best', fontsize=10)
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Lưu file
        chart_path = get_chart_path(city_name_viet, "clouds")
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ độ che phủ mây: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ LỖI vẽ biểu đồ độ che phủ mây: {e}")
        plt.close()
        return None


def create_all_advanced_charts(city_name_viet: str = "Hà Nội") -> Dict[str, Optional[str]]:
    """
    Vẽ tất cả các biểu đồ nâng cao cho một thành phố.
    
    Args:
        city_name_viet: Tên thành phố tiếng Việt
    
    Returns:
        Dict[str, Optional[str]]: Dictionary chứa kết quả vẽ biểu đồ
    """
    
    print("\n" + "="*50)
    print(f"🎨 TRỰC QUAN HÓA NÂNG CAO - {city_name_viet}")
    print("="*50 + "\n")
    
    results = {
        'Áp suất': create_pressure_chart(city_name_viet),
        'Tầm nhìn': create_visibility_chart(city_name_viet),
        'Độ che phủ mây': create_cloud_cover_chart(city_name_viet)
    }
    
    print("\n" + "="*50)
    print("📊 KẾT QUẢ VẼ BIỂU ĐỒ NÂNG CAO:")
    print("="*50)
    for name, path in results.items():
        status = "✅ Thành công" if path else "❌ Thất bại"
        print(f"{name:30} {status}")
    
    return results


if __name__ == "__main__":
    # Chạy thử
    create_all_advanced_charts("Hà Nội")


