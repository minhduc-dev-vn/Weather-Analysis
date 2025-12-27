"""
Ứng dụng GUI Dự Báo Thời Tiết - Weather Forecast Pro

Giao diện desktop sử dụng Tkinter để:
    - Lấy dữ liệu thời tiết từ API OpenWeatherMap
    - Xử lý và làm sạch dữ liệu
    - Vẽ biểu đồ thời tiết
    - Hiển thị trực quan hóa dữ liệu

Author: Weather Forecast Pro Team
Date: 2025-12-27
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pandas as pd

# Import các module xử lý dữ liệu
import src.data_loader as loader
import src.data_cleaner as cleaner
import src.visualizer as vis
import src.statistics as stats
from src.config import CHART_PATH, CITY_NAME


class WeatherApp:
    """
    Ứng dụng GUI dự báo thời tiết.
    
    Attributes:
        root: Cửa sổ Tkinter chính
        lbl_title: Nhãn tiêu đề
        btn_update: Nút cập nhật dữ liệu
        lbl_status: Nhãn trạng thái
        chart_frame: Khung chứa biểu đồ
        lbl_chart_img: Nhãn hiển thị ảnh biểu đồ
    """
    
    def __init__(self, root: tk.Tk):
        """
        Khởi tạo ứng dụng.
        
        Args:
            root: Cửa sổ Tkinter chính
        """
        self.root = root
        self.root.title(f"🌦️ Dự Báo Thời Tiết - {CITY_NAME}")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # --- 1. TIÊU ĐỀ ---
        self.lbl_title = tk.Label(
            root, 
            text=f"🌍 HỆ THỐNG PHÂN TÍCH VÀ DỰ BÁO THỜI TIẾT: {CITY_NAME}",
            font=("Arial", 20, "bold"), 
            fg="#1976D2",
            bg="#E3F2FD"
        )
        self.lbl_title.pack(pady=15, fill="x")
        
        # --- 2. KHUNG NÚT BẤM ---
        button_frame = tk.Frame(root, bg="#f5f5f5")
        button_frame.pack(pady=10, fill="x", padx=10)
        
        self.btn_update = tk.Button(
            button_frame,
            text="🔄 Cập Nhật Dữ Liệu Mới Nhất",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.update_data,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_update.pack(side="left", padx=5)
        
        self.btn_stats = tk.Button(
            button_frame,
            text="📊 Xem Thống Kê",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.show_statistics,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_stats.pack(side="left", padx=5)
        
        # --- 3. KHUNG TRẠNG THÁI ---
        self.lbl_status = tk.Label(
            root,
            text="✓ Trạng thái: Sẵn sàng",
            font=("Arial", 10, "italic"),
            fg="#666",
            bg="#fff"
        )
        self.lbl_status.pack(pady=5, fill="x", padx=10)
        
        # --- 4. KHUNG HIỂN THỊ BIỂU ĐỒ ---
        self.chart_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="sunken")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_chart_img = tk.Label(
            self.chart_frame,
            text="💾 Vui lòng bấm 'Cập Nhật Dữ Liệu Mới Nhất' để xem biểu đồ",
            bg="#f0f0f0",
            font=("Arial", 12, "italic"),
            fg="#666"
        )
        self.lbl_chart_img.pack(expand=True)

    def update_data(self) -> None:
        """
        Cập nhật dữ liệu: Tải API → Làm sạch → Vẽ biểu đồ → Hiển thị
        
        Quy trình:
        1. Lấy dữ liệu từ API OpenWeatherMap
        2. Xử lý và làm sạch dữ liệu
        3. Vẽ các biểu đồ (chính + histogram + tốc gió)
        4. Hiển thị biểu đồ chính lên giao diện
        5. Hiển thị thông báo kết quả
        """
        
        try:
            # ===== BƯỚC 1: LẤY DỮ LIỆU =====
            self.lbl_status.config(
                text="⏳ Đang tải dữ liệu từ API OpenWeatherMap...",
                fg="blue"
            )
            self.root.update()
            
            df_raw = loader.fetch_weather_data()
            
            if df_raw is None:
                self.lbl_status.config(
                    text="❌ Lỗi: Không lấy được dữ liệu. Kiểm tra API Key hoặc Internet",
                    fg="red"
                )
                messagebox.showerror(
                    "Lỗi Kết Nối",
                    "❌ Không thể kết nối API OpenWeatherMap\n\n"
                    "Các lý do có thể:\n"
                    "1. API Key sai hoặc chưa được kích hoạt\n"
                    "2. Tên thành phố sai\n"
                    "3. Không có kết nối Internet\n"
                    "4. API server bị lỗi\n\n"
                    "Vui lòng kiểm tra và thử lại"
                )
                return
            
            # ===== BƯỚC 2: LÀM SẠCH DỮ LIỆU =====
            self.lbl_status.config(
                text="🧹 Đang xử lý và làm sạch dữ liệu...",
                fg="orange"
            )
            self.root.update()
            
            df_clean = cleaner.clean_data()
            
            if df_clean is None:
                self.lbl_status.config(
                    text="❌ Lỗi xử lý dữ liệu",
                    fg="red"
                )
                messagebox.showerror(
                    "Lỗi Xử Lý",
                    "❌ Không thể xử lý dữ liệu\n\n"
                    "Vui lòng thử lại"
                )
                return
            
            # ===== BƯỚC 3: VẼ BIỂU ĐỒ =====
            self.lbl_status.config(
                text="📊 Đang vẽ biểu đồ (có thể mất vài giây)...",
                fg="purple"
            )
            self.root.update()
            
            # Vẽ tất cả biểu đồ
            success = vis.create_all_charts()
            
            if not success:
                self.lbl_status.config(
                    text="⚠️ Cảnh báo: Một số biểu đồ không vẽ được",
                    fg="orange"
                )
            
            # ===== BƯỚC 4: HIỂN THỊ BIỂU ĐỒ =====
            if os.path.exists(CHART_PATH):
                self.show_chart_image()
                current_time = pd.Timestamp.now().strftime('%H:%M:%S')
                self.lbl_status.config(
                    text=f"✅ Cập nhật thành công lúc {current_time}",
                    fg="green"
                )
                
                messagebox.showinfo(
                    "Thành Công",
                    f"✅ Đã cập nhật dữ liệu thời tiết mới nhất!\n\n"
                    f"Thành phố: {CITY_NAME}\n"
                    f"Tổng bản ghi: {len(df_clean)}\n"
                    f"Thời gian: {current_time}"
                )
            else:
                self.lbl_status.config(
                    text="❌ Lỗi: Không tìm thấy file biểu đồ",
                    fg="red"
                )
                
        except Exception as e:
            self.lbl_status.config(
                text=f"❌ Lỗi không xác định: {str(e)[:50]}...",
                fg="red"
            )
            messagebox.showerror(
                "Lỗi",
                f"❌ Lỗi không xác định:\n{str(e)}"
            )

    def show_chart_image(self) -> None:
        """
        Đọc ảnh biểu đồ từ file và hiển thị lên giao diện.
        
        Note:
            - Resize ảnh để vừa khung
            - Giữ tỉ lệ khung hình
        """
        try:
            # Mở ảnh từ file
            img = Image.open(CHART_PATH)
            
            # Resize với tỉ lệ 4:3
            img = img.resize((900, 600), Image.Resampling.LANCZOS)
            
            # Chuyển sang định dạng Tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Hiển thị lên label
            self.lbl_chart_img.config(image=photo, text="")
            self.lbl_chart_img.image = photo  # Giữ tham chiếu quan trọng!
            
        except Exception as e:
            self.lbl_status.config(
                text=f"❌ Lỗi hiển thị ảnh: {e}",
                fg="red"
            )

    def show_statistics(self) -> None:
        """
        Hiển thị cửa sổ thống kê chi tiết.
        """
        try:
            print("\n" + "="*70)
            print("Đang tạo báo cáo thống kê...")
            print("="*70 + "\n")
            
            stats.print_full_statistics()
            
            messagebox.showinfo(
                "Thống Kê",
                "✅ Báo cáo thống kê đã được in ra terminal\n\n"
                "Kiểm tra cửa sổ terminal để xem chi tiết!"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"❌ Không thể tạo báo cáo thống kê:\n{e}"
            )


def main() -> None:
    """
    Hàm chính - khởi động ứng dụng GUI.
    """
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()