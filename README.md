# 🌦️ WEATHER FORECAST PRO - HỆ THỐNG PHÂN TÍCH VÀ DỰ BÁO THỜI TIẾT

**Weather Forecast Pro** là một ứng dụng desktop mạnh mẽ được xây dựng bằng Python, giúp người dùng theo dõi, phân tích và dự báo thời tiết cho các thành phố lớn tại Việt Nam. Phiên bản v3.0 mang đến giao diện hiện đại, khả năng xử lý dữ liệu mạnh mẽ và các biểu đồ trực quan.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng nổi bật](#-tính-năng-nổi-bật)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Mô tả dữ liệu](#-mô-tả-dữ-liệu)
- [Xử lý lỗi thường gặp](#-xử-lý-lỗi-thường-gặp)
- [Tác giả](#-tác-giả)

---

## 📌 Giới thiệu

Weather Forecast Pro được thiết kế để cung cấp thông tin thời tiết chính xác và chi tiết. Ứng dụng không chỉ hiển thị dự báo mà còn cung cấp các công cụ phân tích sâu thông qua biểu đồ và số liệu thống kê.

**Mục tiêu:** Giúp người dùng có cái nhìn tổng quan và chi tiết về xu hướng thời tiết để lên kế hoạch sinh hoạt và làm việc hiệu quả.

---

## ✨ Tính năng nổi bật

- **🌍 Đa dạng địa điểm**: Hỗ trợ theo dõi thời tiết tại 11 thành phố lớn: Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ, Nha Trang, Huế, Quy Nhơn, Phan Thiết, Đà Lạt, Hạ Long, và nhiều hơn nữa.
- **📡 Dữ liệu thời gian thực**: Kết nối API OpenWeatherMap để lấy dữ liệu dự báo 5 ngày (cập nhật 3 giờ/lần).
- **📊 Trực quan hóa dữ liệu**: Hệ thống biểu đồ phong phú:
    - Biểu đồ đường (Nhiệt độ, Độ ẩm)
    - Biểu đồ cột/Histogram (Phân bố nhiệt độ)
    - Biểu đồ Boxplot (So sánh các thành phố)
    - Biểu đồ nâng cao: Áp suất, Tầm nhìn, Độ che phủ mây.
- **📈 Phân tích thống kê**: Tự động tính toán các chỉ số quan trọng: Trung bình, Độ lệch chuẩn, Min/Max.
- **🔀 So sánh đa điểm**: Chế độ so sánh cho phép đối chiếu thời tiết giữa nhiều thành phố cùng lúc.
- **🖥️ Giao diện thân thiện**: Thiết kế dạng tab hiện đại, dễ dàng điều hướng.

---

## 💻 Yêu cầu hệ thống

- **Hệ điều hành**: Windows, macOS, hoặc Linux.
- **Python**: Phiên bản 3.7 trở lên.
- **Kết nối Internet**: Cần thiết để lấy dữ liệu từ API.
- **API Key**: Tài khoản OpenWeatherMap (miễn phí).

---

## 🛠️ Cài đặt

Làm theo các bước sau để cài đặt và chạy ứng dụng:

### 1. Tải dự án
```bash
git clone https://github.com/username/Weather_Forecast_Pro.git
cd Weather_Forecast_Pro
```

### 2. Thiết lập môi trường ảo (Khuyên dùng)
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key
1. Đăng ký tài khoản và lấy key tại [OpenWeatherMap](https://openweathermap.org/api).
2. Mở file `src/config.py` và cập nhật:
   ```python
   API_KEY = "YOUR_API_KEY_HERE"
   ```

### 5. Khởi chạy ứng dụng
```bash
python main.py
```

---

## 🚀 Hướng dẫn sử dụng

### Quy trình cơ bản
1. **Chọn thành phố**: Sử dụng menu thả xuống để chọn thành phố bạn quan tâm.
2. **Cập nhật dữ liệu**: Nhấn nút **"🔄 Cập Nhật Dữ Liệu"**.
   - Ứng dụng sẽ tải dữ liệu mới nhất, xử lý và lưu trữ.
   - Các biểu đồ sẽ được vẽ lại tự động.
3. **Xem chi tiết**:
   - **Tab Tổng quan**: Xem biểu đồ nhiệt độ, độ ẩm, tốc độ gió.
   - **Tab Nâng cao**: Xem áp suất, tầm nhìn, mây.
   - **Tab So sánh**: Chọn nhiều thành phố để so sánh.
   - **Tab Thống kê**: Xem các chỉ số phân tích cụ thể.

---

## 📂 Cấu trúc dự án

```
Weather_Forecast_Pro/
├── assets/                    # Chứa tài nguyên ảnh/biểu đồ
├── data/                      # Kho dữ liệu
│   ├── raw/                   # Dữ liệu thô (CSV) từ API
│   └── processed/             # Dữ liệu đã làm sạch
├── src/                       # Mã nguồn chính
│   ├── __init__.py
│   ├── column_names.py        # Định nghĩa tên cột (Việt/Anh)
│   ├── config.py              # Cấu hình hệ thống (API Key, City List)
│   ├── constants.py           # Các hằng số dùng chung
│   ├── data_cleaner.py        # Module xử lý và làm sạch dữ liệu
│   ├── data_loader.py         # Module tải dữ liệu từ API
│   ├── exceptions.py          # Các ngoại lệ tùy chỉnh
│   ├── logger.py              # Hệ thống ghi log
│   ├── multi_city_analyzer.py # Phân tích so sánh nhiều thành phố
│   ├── plot_helpers.py        # Các hàm hỗ trợ vẽ biểu đồ
│   ├── statistics.py          # Module tính toán thống kê
│   ├── visualizer.py          # Module vẽ biểu đồ cơ bản
│   └── visualizer_advanced.py # Module vẽ biểu đồ nâng cao
├── venv/                      # Môi trường ảo (không commit)
├── main.py                    # File khởi chạy chương trình (GUI)
├── requirements.txt           # Các gói phụ thuộc
├── WORK_DISTRIBUTION.md       # Phân công công việc
└── README.md                  # Tài liệu hướng dẫn
```

---

## 📝 Mô tả dữ liệu (Data Dictionary)

Dữ liệu được lấy từ OpenWeatherMap và chuẩn hóa như sau:

| Tên cột (Raw) | Tên Việt | Đơn vị | Mô tả |
|---|---|---|---|
| `dt_txt` | Thời Gian | YYYY-MM-DD HH:MM:SS | Thời điểm dự báo |
| `temp` | Nhiệt Độ | °C | Nhiệt độ thực tế |
| `feels_like` | Nhiệt Độ Cảm Nhận | °C | Nhiệt độ cơ thể cảm nhận |
| `humidity` | Độ Ẩm | % | Độ ẩm tương đối |
| `pressure` | Áp Suất | hPa | Áp suất khí quyển |
| `wind_speed` | Tốc Gió | m/s | Tốc độ gió |
| `wind_deg` | Hướng Gió | Độ (°) | Hướng gió thổi |
| `clouds` | Mây | % | Độ che phủ của mây |
| `visibility` | Tầm Nhìn | km | Khoảng cách nhìn xa |
| `description` | Mô Tả | Text | Trạng thái thời tiết (mưa, nắng...) |

---

## ⚠️ Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| **401 Unauthorized** | API Key sai hoặc chưa kích hoạt | Kiểm tra lại `src/config.py`. API Key mới cần vài giờ để kích hoạt. |
| **Connection Error** | Mất kết nối mạng | Kiểm tra Internet của bạn. |
| **ModuleNotFoundError** | Chưa cài thư viện | Chạy lại `pip install -r requirements.txt`. |
| **Empty Data** | Lỗi dữ liệu/Tên thành phố | Kiểm tra tên thành phố hoặc thử lại sau. |

---

## 👥 Tác giả

Dự án được thực hiện bởi nhóm sinh viên lớp **Lập trình Python (IPPA233277)**:
- Vũ Minh Đức
- Phan Tiến Đạt

- **Ngày thực hiện:** Tháng 12/2025
---
*Cảm ơn bạn đã quan tâm đến dự án Weather Forecast Pro!* 🌦️
