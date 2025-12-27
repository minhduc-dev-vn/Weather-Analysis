"""
Ứng dụng GUI Dự Báo Thời Tiết - Weather Forecast Pro v3.0

Giao diện desktop nâng cấp với Tkinter:
    - Hỗ trợ nhiều thành phố Việt Nam
    - Tabbed interface cho nhiều biểu đồ
    - Tổng quan tất cả thành phố
    - Giao diện đẹp mắt, hiện đại

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import pandas as pd
import threading

# Import các module xử lý dữ liệu
import src.data_loader as loader
import src.data_cleaner as cleaner
import src.visualizer as vis
import src.visualizer_advanced as vis_adv
import src.statistics as stats
from src.config import (
    VIETNAM_CITIES, DEFAULT_CITY_VIET, 
    get_chart_path, get_processed_data_path
)


class WeatherApp:
    """
    Ứng dụng GUI dự báo thời tiết với nhiều tính năng nâng cao.
    
    Features:
        - Chọn thành phố từ dropdown
        - Tabbed interface với nhiều loại biểu đồ
        - Tổng quan tất cả thành phố
        - Nút quay lại để thay đổi biểu đồ
        - Giao diện đẹp mắt, hiện đại
    """
    
    def __init__(self, root: tk.Tk):
        """
        Khởi tạo ứng dụng.
        
        Args:
            root: Cửa sổ Tkinter chính
        """
        self.root = root
        self.root.title("🌦️ Weather Forecast Pro - Hệ Thống Dự Báo Thời Tiết")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Màu sắc chủ đạo
        self.colors = {
            'primary': '#1976D2',
            'secondary': '#42A5F5',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'background': '#F5F5F5',
            'card': '#FFFFFF'
        }
        
        # Thành phố hiện tại
        self.current_city = DEFAULT_CITY_VIET
        
        # Tạo giao diện
        self.create_ui()
    
    def create_ui(self):
        """Tạo giao diện người dùng."""
        
        # --- HEADER ---
        header_frame = tk.Frame(
            self.root, 
            bg=self.colors['primary'],
            height=80
        )
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🌍 HỆ THỐNG PHÂN TÍCH VÀ DỰ BÁO THỜI TIẾT",
            font=("Arial", 22, "bold"),
            fg="white",
            bg=self.colors['primary']
        )
        title_label.pack(pady=20)
        
        # --- CONTROL PANEL ---
        control_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=10)
        control_frame.pack(fill="x")
        
        # Chọn thành phố
        city_label = tk.Label(
            control_frame,
            text="📍 Chọn thành phố:",
            font=("Arial", 11, "bold"),
            bg=self.colors['background']
        )
        city_label.pack(side="left", padx=(0, 10))
        
        self.city_var = tk.StringVar(value=self.current_city)
        city_combo = ttk.Combobox(
            control_frame,
            textvariable=self.city_var,
            values=list(VIETNAM_CITIES.keys()),
            state="readonly",
            width=25,
            font=("Arial", 11)
        )
        city_combo.pack(side="left", padx=(0, 20))
        city_combo.bind("<<ComboboxSelected>>", self.on_city_change)
        
        # Nút cập nhật dữ liệu
        self.btn_update = tk.Button(
            control_frame,
            text="🔄 Cập Nhật Dữ Liệu",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg="white",
            command=self.update_data_threaded,
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
            bd=0
        )
        self.btn_update.pack(side="left", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="✓ Sẵn sàng")
        status_label = tk.Label(
            control_frame,
            textvariable=self.status_var,
            font=("Arial", 10, "italic"),
            fg="#666",
            bg=self.colors['background']
        )
        status_label.pack(side="right", padx=20)
        
        # --- NOTEBOOK (TABBED INTERFACE) ---
        notebook_frame = tk.Frame(self.root, bg=self.colors['background'])
        notebook_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['background'], borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 11, 'bold'))
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Biểu đồ chính
        self.create_main_chart_tab()
        
        # Tab 2: Biểu đồ nâng cao
        self.create_advanced_charts_tab()
        
        # Tab 3: Tổng quan tất cả thành phố
        self.create_overview_tab()
        
        # Tab 4: Thống kê chi tiết
        self.create_statistics_tab()
    
    def create_main_chart_tab(self):
        """Tạo tab biểu đồ chính."""
        tab1_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(tab1_frame, text="📊 Biểu Đồ Chính")
        
        # Nút vẽ biểu đồ (TRÊN CÙNG)
        btn_frame = tk.Frame(tab1_frame, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="📈 Vẽ Biểu Đồ Chính",
            font=("Arial", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            command=lambda: self.show_chart("main", self.main_chart_label),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📊 Histogram",
            font=("Arial", 10, "bold"),
            bg=self.colors['secondary'],
            fg="white",
            command=lambda: self.show_chart("histogram", self.main_chart_label),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="💨 Tốc Gió",
            font=("Arial", 10, "bold"),
            bg=self.colors['warning'],
            fg="white",
            command=lambda: self.show_chart("wind", self.main_chart_label),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)
        
        # Nút quay lại
        tk.Button(
            btn_frame,
            text="⬅️ Quay Lại",
            font=("Arial", 10, "bold"),
            bg=self.colors['danger'],
            fg="white",
            command=lambda: self.clear_chart(self.main_chart_label),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="right", padx=5)
        
        # Frame chứa biểu đồ (Ở GIỮA)
        chart_container = tk.Frame(tab1_frame, bg=self.colors['card'])
        chart_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Label hiển thị biểu đồ
        self.main_chart_label = tk.Label(
            chart_container,
            text="💾 Vui lòng chọn biểu đồ để xem",
            bg=self.colors['card'],
            font=("Arial", 12, "italic"),
            fg="#999"
        )
        self.main_chart_label.pack(expand=True)
    
    def create_advanced_charts_tab(self):
        """Tạo tab biểu đồ nâng cao."""
        tab2_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(tab2_frame, text="📈 Biểu Đồ Nâng Cao")
        
        # Nút vẽ biểu đồ nâng cao (TRÊN CÙNG)
        btn_frame = tk.Frame(tab2_frame, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        btn_configs = [
            ("� Áp Suất", "pressure", self.colors['primary']),
            ("�️ Tầm Nhìn", "visibility", self.colors['warning']),
            ("☁️ Độ Che Phủ Mây", "clouds", self.colors['secondary'])
        ]
        
        for text, chart_type, color in btn_configs:
            tk.Button(
                btn_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                command=lambda ct=chart_type: self.show_advanced_chart(ct),
                padx=15,
                pady=8,
                cursor="hand2",
                relief="flat"
            ).pack(side="left", padx=5)
        
        # Nút quay lại
        tk.Button(
            btn_frame,
            text="⬅️ Quay Lại",
            font=("Arial", 10, "bold"),
            bg=self.colors['danger'],
            fg="white",
            command=lambda: self.clear_chart(self.advanced_chart_label),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="right", padx=5)
        
        # Frame chứa biểu đồ (Ở GIỮA)
        chart_container = tk.Frame(tab2_frame, bg=self.colors['card'])
        chart_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.advanced_chart_label = tk.Label(
            chart_container,
            text="💾 Vui lòng chọn loại biểu đồ để xem",
            bg=self.colors['card'],
            font=("Arial", 12, "italic"),
            fg="#999"
        )
        self.advanced_chart_label.pack(expand=True)
    
    def create_overview_tab(self):
        """Tạo tab tổng quan tất cả thành phố."""
        tab3_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(tab3_frame, text="🌍 Tổng Quan Tất Cả Thành Phố")
        
        # Frame chứa nội dung
        content_frame = tk.Frame(tab3_frame, bg=self.colors['card'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Text widget để hiển thị bảng tổng quan
        overview_text_frame = tk.Frame(content_frame, bg=self.colors['card'])
        overview_text_frame.pack(fill="both", expand=True)
        
        # Scrollbar (pack TRƯỚC)
        scrollbar = tk.Scrollbar(overview_text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.overview_text = tk.Text(
            overview_text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="white",
            relief="sunken",
            bd=2,
            yscrollcommand=scrollbar.set
        )
        self.overview_text.pack(fill="both", expand=True)
        
        scrollbar.config(command=self.overview_text.yview)
        
        # Nút làm mới tổng quan
        btn_frame = tk.Frame(tab3_frame, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="🔄 Làm Mới Tổng Quan",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg="white",
            command=self.refresh_overview,
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)
        
        # Hiển thị tổng quan ban đầu
        self.overview_text.insert("1.0", "💾 Vui lòng cập nhật dữ liệu cho các thành phố và bấm 'Làm Mới Tổng Quan' để xem bảng tổng quan.")
        self.overview_text.config(state="disabled")
    
    def create_statistics_tab(self):
        """Tạo tab thống kê."""
        tab4_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(tab4_frame, text="📋 Thống Kê")
        
        # Text widget để hiển thị thống kê
        stats_text_frame = tk.Frame(tab4_frame, bg=self.colors['card'])
        stats_text_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scrollbar (pack TRƯỚC)
        scrollbar = tk.Scrollbar(stats_text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.stats_text = tk.Text(
            stats_text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="white",
            relief="sunken",
            bd=2,
            yscrollcommand=scrollbar.set
        )
        self.stats_text.pack(fill="both", expand=True)
        
        scrollbar.config(command=self.stats_text.yview)
        
        # Nút làm mới thống kê
        btn_frame = tk.Frame(tab4_frame, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="🔄 Làm Mới Thống Kê",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg="white",
            command=self.refresh_statistics,
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)
        
        # Hiển thị thống kê ban đầu
        self.stats_text.insert("1.0", "Vui lòng chọn thành phố và bấm 'Làm Mới Thống Kê' để xem thống kê chi tiết.")
        self.stats_text.config(state="disabled")
    
    def on_city_change(self, event=None):
        """Xử lý khi thay đổi thành phố."""
        self.current_city = self.city_var.get()
        self.status_var.set(f"✓ Đã chọn: {self.current_city}")
    
    def update_data_threaded(self):
        """Cập nhật dữ liệu trong thread riêng để không block GUI."""
        self.btn_update.config(state="disabled")
        self.status_var.set("⏳ Đang tải dữ liệu...")
        
        thread = threading.Thread(target=self.update_data)
        thread.daemon = True
        thread.start()
    
    def update_data(self):
        """Cập nhật dữ liệu thời tiết."""
        try:
            city = self.current_city
            
            # Bước 1: Lấy dữ liệu
            self.root.after(0, lambda: self.status_var.set(f"⏳ Đang tải dữ liệu cho {city}..."))
            df_raw = loader.fetch_weather_data(city)
            
            if df_raw is None:
                self.root.after(0, lambda: self.status_var.set("❌ Lỗi: Không lấy được dữ liệu"))
                self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ API"))
                self.root.after(0, lambda: self.btn_update.config(state="normal"))
                return
            
            # Bước 2: Làm sạch dữ liệu
            self.root.after(0, lambda: self.status_var.set("🧹 Đang xử lý dữ liệu..."))
            df_clean = cleaner.clean_data(city)
            
            if df_clean is None:
                self.root.after(0, lambda: self.status_var.set("❌ Lỗi xử lý dữ liệu"))
                self.root.after(0, lambda: self.btn_update.config(state="normal"))
                return
            
            # Bước 3: Vẽ biểu đồ
            self.root.after(0, lambda: self.status_var.set("📊 Đang vẽ biểu đồ..."))
            vis.create_all_charts(city)
            vis_adv.create_all_advanced_charts(city)
            
            # Thành công
            self.root.after(0, lambda: self.status_var.set(f"✅ Đã cập nhật dữ liệu cho {city}"))
            self.root.after(0, lambda: messagebox.showinfo("Thành công", f"Đã cập nhật dữ liệu cho {city}!"))
            self.root.after(0, lambda: self.btn_update.config(state="normal"))
            
            # Tự động hiển thị biểu đồ chính
            self.root.after(100, lambda: self.show_chart("main", self.main_chart_label))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Lỗi: {str(e)[:50]}"))
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi không xác định:\n{str(e)}"))
            self.root.after(0, lambda: self.btn_update.config(state="normal"))
    
    def show_chart(self, chart_type: str, label_widget: tk.Label):
        """Hiển thị biểu đồ."""
        try:
            chart_path = get_chart_path(self.current_city, chart_type)
            
            if not os.path.exists(chart_path):
                messagebox.showwarning("Cảnh báo", f"Chưa có biểu đồ {chart_type}. Vui lòng cập nhật dữ liệu trước.")
                return
            
            img = Image.open(chart_path)
            img = img.resize((1000, 650), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            label_widget.config(image=photo, text="")
            label_widget.image = photo
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị biểu đồ:\n{str(e)}")
    
    def show_advanced_chart(self, chart_type: str):
        """Hiển thị biểu đồ nâng cao."""
        try:
            chart_path = get_chart_path(self.current_city, chart_type)
            
            if not os.path.exists(chart_path):
                messagebox.showwarning("Cảnh báo", f"Chưa có biểu đồ {chart_type}.\nVui lòng cập nhật dữ liệu trước.")
                return
            
            img = Image.open(chart_path)
            img = img.resize((1000, 650), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.advanced_chart_label.config(image=photo, text="")
            self.advanced_chart_label.image = photo
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị biểu đồ:\n{str(e)}")
    
    def clear_chart(self, label_widget: tk.Label):
        """Xóa biểu đồ hiện tại và quay lại trạng thái ban đầu."""
        label_widget.config(image="", text="💾 Vui lòng chọn biểu đồ để xem")
        label_widget.image = None
    
    def refresh_overview(self):
        """Làm mới tổng quan tất cả thành phố."""
        try:
            # Lấy danh sách tất cả thành phố có dữ liệu
            all_cities = list(VIETNAM_CITIES.keys())
            cities_with_data = []
            
            for city in all_cities:
                processed_path = get_processed_data_path(city)
                if os.path.exists(processed_path):
                    cities_with_data.append(city)
            
            if len(cities_with_data) == 0:
                self.overview_text.config(state="normal")
                self.overview_text.delete("1.0", tk.END)
                self.overview_text.insert("1.0", "⚠️ Chưa có dữ liệu cho thành phố nào.\nVui lòng cập nhật dữ liệu cho ít nhất một thành phố.")
                self.overview_text.config(state="disabled")
                return
            
            # Tạo bảng tổng quan
            overview_text = self.generate_overview_text(cities_with_data)
            
            self.overview_text.config(state="normal")
            self.overview_text.delete("1.0", tk.END)
            self.overview_text.insert("1.0", overview_text)
            self.overview_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tạo tổng quan:\n{str(e)}")
    
    def generate_overview_text(self, city_list: list) -> str:
        """Tạo văn bản tổng quan cho tất cả thành phố."""
        text = f"{'='*80}\n"
        text += f"{' '*25}🌍 TỔNG QUAN TẤT CẢ THÀNH PHỐ\n"
        text += f"{'='*80}\n\n"
        
        text += f"📍 Tổng số thành phố có dữ liệu: {len(city_list)}\n"
        text += f"📅 Thời gian: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Bảng tổng quan theo metric
        metrics = ['Nhiệt Độ', 'Độ Ẩm', 'Tốc Gió', 'Áp Suất']
        
        for metric in metrics:
            text += f"\n{'='*80}\n"
            text += f"📊 {metric.upper()}\n"
            text += f"{'='*80}\n"
            text += f"{'Thành Phố':<25} {'Trung Bình':<15} {'Cao Nhất':<15} {'Thấp Nhất':<15}\n"
            text += "-" * 80 + "\n"
            
            city_stats = []
            for city in city_list:
                try:
                    processed_path = get_processed_data_path(city)
                    df = pd.read_csv(processed_path)
                    
                    if metric in df.columns:
                        mean_val = df[metric].mean()
                        max_val = df[metric].max()
                        min_val = df[metric].min()
                        
                        city_stats.append({
                            'city': city,
                            'mean': mean_val,
                            'max': max_val,
                            'min': min_val
                        })
                except:
                    continue
            
            # Sắp xếp theo trung bình (cao đến thấp)
            city_stats.sort(key=lambda x: x['mean'], reverse=True)
            
            for stat in city_stats:
                if metric == 'Nhiệt Độ':
                    text += f"{stat['city']:<25} {stat['mean']:>12.1f}°C  {stat['max']:>12.1f}°C  {stat['min']:>12.1f}°C\n"
                elif metric == 'Độ Ẩm':
                    text += f"{stat['city']:<25} {stat['mean']:>12.0f}%   {stat['max']:>12.0f}%   {stat['min']:>12.0f}%\n"
                elif metric == 'Tốc Gió':
                    text += f"{stat['city']:<25} {stat['mean']:>11.2f} m/s  {stat['max']:>11.2f} m/s  {stat['min']:>11.2f} m/s\n"
                elif metric == 'Áp Suất':
                    text += f"{stat['city']:<25} {stat['mean']:>12.0f} hPa {stat['max']:>12.0f} hPa {stat['min']:>12.0f} hPa\n"
            
            # Tìm thành phố cao nhất và thấp nhất
            if city_stats:
                max_city = city_stats[0]
                min_city = city_stats[-1]
                text += f"\n🏆 Thành phố {metric} cao nhất: {max_city['city']} ({max_city['mean']:.2f})\n"
                text += f"📉 Thành phố {metric} thấp nhất: {min_city['city']} ({min_city['mean']:.2f})\n"
        
        text += f"\n{'='*80}\n"
        text += f"\n💡 Lưu ý: Dữ liệu được cập nhật theo thời gian thực từ API OpenWeatherMap\n"
        
        return text
    
    def show_statistics(self):
        """Hiển thị cửa sổ thống kê."""
        self.refresh_statistics()
        self.notebook.select(3)  # Chuyển sang tab thống kê (index 3)
    
    def refresh_statistics(self):
        """Làm mới thống kê."""
        try:
            processed_path = get_processed_data_path(self.current_city)
            
            if not os.path.exists(processed_path):
                self.stats_text.config(state="normal")
                self.stats_text.delete("1.0", tk.END)
                self.stats_text.insert("1.0", f"⚠️ Chưa có dữ liệu cho {self.current_city}.\nVui lòng cập nhật dữ liệu trước.")
                self.stats_text.config(state="disabled")
                return
            
            df = pd.read_csv(processed_path)
            df['Thời Gian'] = pd.to_datetime(df['Thời Gian'])
            
            # Tạo báo cáo thống kê
            stats_report = self.generate_statistics_text(df)
            
            self.stats_text.config(state="normal")
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("1.0", stats_report)
            self.stats_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tạo thống kê:\n{str(e)}")
    
    def generate_statistics_text(self, df: pd.DataFrame) -> str:
        """Tạo văn bản thống kê từ DataFrame."""
        text = f"{'='*70}\n"
        text += f"{' '*20}📊 BÁO CÁO THỐNG KÊ - {self.current_city}\n"
        text += f"{'='*70}\n\n"
        
        # Thông tin thời gian
        text += "📅 THÔNG TIN THỜI GIAN:\n"
        text += f"  • Từ:        {df['Thời Gian'].min()}\n"
        text += f"  • Đến:       {df['Thời Gian'].max()}\n"
        text += f"  • Tổng mốc:  {len(df)} mốc\n\n"
        
        # Thống kê nhiệt độ
        if 'Nhiệt Độ' in df.columns:
            text += "🌡️ THỐNG KÊ NHIỆT ĐỘ:\n"
            text += f"  • Trung bình:  {df['Nhiệt Độ'].mean():.1f}°C\n"
            text += f"  • Cao nhất:    {df['Nhiệt Độ'].max():.1f}°C\n"
            text += f"  • Thấp nhất:   {df['Nhiệt Độ'].min():.1f}°C\n"
            text += f"  • Độ lệch:     {df['Nhiệt Độ'].std():.1f}°C\n\n"
        
        # Thống kê độ ẩm
        if 'Độ Ẩm' in df.columns:
            text += "💧 THỐNG KÊ ĐỘ ẨM:\n"
            text += f"  • Trung bình:  {df['Độ Ẩm'].mean():.0f}%\n"
            text += f"  • Cao nhất:    {df['Độ Ẩm'].max()}%\n"
            text += f"  • Thấp nhất:   {df['Độ Ẩm'].min()}%\n\n"
        
        # Thống kê tốc gió
        if 'Tốc Gió' in df.columns:
            text += "💨 THỐNG KÊ TỐC GIÓ:\n"
            text += f"  • Trung bình:  {df['Tốc Gió'].mean():.2f} m/s\n"
            text += f"  • Cao nhất:    {df['Tốc Gió'].max():.2f} m/s\n"
            text += f"  • Thấp nhất:   {df['Tốc Gió'].min():.2f} m/s\n\n"
        
        # Thống kê áp suất
        if 'Áp Suất' in df.columns:
            text += "📊 THỐNG KÊ ÁP SUẤT:\n"
            text += f"  • Trung bình:  {df['Áp Suất'].mean():.0f} hPa\n"
            text += f"  • Cao nhất:    {df['Áp Suất'].max()} hPa\n"
            text += f"  • Thấp nhất:   {df['Áp Suất'].min()} hPa\n\n"
        
        text += f"{'='*70}\n"
        
        return text


def main() -> None:
    """
    Hàm chính - khởi động ứng dụng GUI.
    """
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
