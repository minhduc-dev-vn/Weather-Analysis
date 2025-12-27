# 🌦️ HỆ THỐNG PHÂN TÍCH VÀ DỰ BÁO THỜI TIẾT (Weather Forecast Pro)

## 📌 1. Giới thiệu dự án

**Hệ Thống Phân Tích Và Dự Báo Thời Tiết v3.0** là ứng dụng desktop Python với nhiều tính năng nâng cao:

- 🌍 **Hỗ trợ 11 thành phố Việt Nam** (Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ, Nha Trang, Huế, Vũng Tàu, Quy Nhon, Phan Thiet, Đà Lạt, Hạ Long)
- 📡 **Lấy dữ liệu thời tiết** từ API OpenWeatherMap (5 ngày, cập nhật 3 giờ/lần) với nhiều metric
- 🧹 **Xử lý và làm sạch dữ liệu** (loại bỏ lỗi, chuẩn hóa định dạng)
- 📊 **Nhiều loại biểu đồ** (đường, cột, histogram, áp suất, tầm nhìn, độ che phủ mây)
- 📈 **Phân tích thống kê** chi tiết (trung bình, độ lệch chuẩn, xu hướng)
- 🔀 **So sánh nhiều thành phố** cùng lúc
- 🖥️ **Giao diện hiện đại** với tabbed interface, dễ sử dụng

**Mục đích:** Giúp người dùng hiểu và dự báo xu hướng thời tiết trong tương lai gần.

---

## 📊 2. Mô Tả Dữ Liệu (Data Dictionary)

### Nguồn dữ liệu
- **API:** OpenWeatherMap (https://openweathermap.org)
- **Loại:** Dự báo thời tiết 5 ngày
- **Tần suất cập nhật:** 3 giờ/lần
- **Định dạng trả về:** JSON

### Cấu trúc dữ liệu

| Cột | Tên Việt | Kiểu dữ liệu | Mô tả | Đơn vị |
|-----|---------|---------|-------|--------|
| `dt_txt` | Thời Gian | DateTime | Thời điểm dự báo | YYYY-MM-DD HH:MM:SS |
| `temp` | Nhiệt Độ | Float | Nhiệt độ không khí | °C (Celsius) |
| `feels_like` | Nhiệt Độ Cảm Nhận | Float | Nhiệt độ cảm nhận | °C (Celsius) |
| `humidity` | Độ Ẩm | Integer | Độ ẩm không khí | % (0-100) |
| `pressure` | Áp Suất | Integer | Áp suất khí quyển | hPa (hectoPascal) |
| `wind_speed` | Tốc Gió | Float | Tốc độ gió ngang | m/s (mét/giây) |
| `wind_deg` | Hướng Gió | Integer | Hướng gió | 0-360 độ |
| `clouds` | Độ Che Phủ Mây | Integer | Độ che phủ mây | % (0-100) |
| `visibility` | Tầm Nhìn | Float | Tầm nhìn | km |
| `description` | Mô Tả | String | Mô tả điều kiện thời tiết | Text (mưa, nắng, mây, v.v.) |

### Hạn chế và khiếm khuyết
- ❌ **Yêu cầu API Key:** Phải tạo tài khoản OpenWeatherMap (miễn phí)
- ❌ **Phụ thuộc mạng:** Cần kết nối Internet để lấy dữ liệu
- ❌ **Giới hạn API:** Gói miễn phí có giới hạn 60 lần gọi/phút
- ⚠️ **Dữ liệu lỗi:** Một số thành phố nhỏ có thể trả về dữ liệu không chính xác
- ⚠️ **Múi giờ:** Dữ liệu trả về theo UTC, cần chuyển đổi nếu cần

---

## 🛠️ 3. Cài đặt & Yêu cầu hệ thống

### Yêu cầu
- **Python:** 3.7 trở lên
- **OS:** Windows, macOS, Linux
- **RAM:** Tối thiểu 512 MB
- **Kết nối Internet:** Bắt buộc

### Các bước cài đặt

#### 1. Clone hoặc tải dự án
```bash
git clone https://github.com/username/Weather_Forecast_Pro.git
cd Weather_Forecast_Pro
```

#### 2. Tạo môi trường ảo (Virtual Environment)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

#### 4. Lấy API Key
1. Truy cập: https://openweathermap.org/api
2. Đăng ký tài khoản miễn phí
3. Tạo API Key trong mục "API Keys"
4. Sao chép API Key

#### 5. Cấu hình API Key
Mở file `src/config.py` và thay thế:
```python
API_KEY = "YOUR_API_KEY_HERE"  # Dán API Key của bạn vào đây
```

**Lưu ý:** Bạn có thể chọn thành phố trực tiếp trong giao diện, không cần chỉnh trong config.

#### 6. Chạy ứng dụng

```bash
# Kích hoạt virtual environment
venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # macOS/Linux

# Chạy chương trình
python main.py
```

Sau khi chạy, cửa sổ GUI sẽ hiện ra.

---

## 📋 4. Cấu trúc dự án

```
Weather_Forecast_Pro/
│
├── main.py                    # Ứng dụng GUI chính
├── requirements.txt           # Danh sách thư viện phụ thuộc
├── README.md                  # Tài liệu này
├── CHANGELOG.md               # Lịch sử thay đổi
├── WORK_DISTRIBUTION.md       # Phân công công việc
│
├── src/                       # Mã nguồn chính
│   ├── __init__.py
│   ├── config.py             # Cấu hình (API Key, danh sách thành phố)
│   ├── data_loader.py        # Lấy dữ liệu từ API (nhiều thành phố)
│   ├── data_cleaner.py       # Xử lý & làm sạch dữ liệu
│   ├── visualizer.py         # Vẽ biểu đồ cơ bản
│   ├── visualizer_advanced.py # Vẽ biểu đồ nâng cao (heatmap, boxplot, ...)
│   ├── statistics.py         # Phân tích thống kê
│   └── multi_city_analyzer.py # Phân tích so sánh nhiều thành phố
│
├── data/                      # Lưu trữ dữ liệu (tự động tạo)
│   ├── raw/                  # Dữ liệu thô từ API (theo thành phố)
│   └── processed/            # Dữ liệu đã xử lý (theo thành phố)
│
└── assets/                    # Lưu trữ ảnh/biểu đồ (tự động tạo)
    └── (các file biểu đồ được tạo tự động)
```

---

## 🚀 5. Hướng dẫn sử dụng

### Sơ đồ quy trình
```
┌─────────────────────────────────────────────────┐
│  1. Nhấn "🔄 Cập Nhật Dữ Liệu Mới Nhất"        │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Lấy từ API (JSON)  │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────────────┐
        │  Lưu: weather_raw.csv      │
        └──────────┬──────────────────┘
                   │
        ┌──────────▼──────────────────────┐
        │  Xử lý & Làm sạch dữ liệu     │
        │  (Convert, làm tròn, rename)   │
        └──────────┬──────────────────────┘
                   │
        ┌──────────▼──────────────────┐
        │  Lưu: weather_clean.csv    │
        └──────────┬──────────────────┘
                   │
        ┌──────────▼──────────────────┐
        │  Vẽ biểu đồ (Matplotlib)   │
        └──────────┬──────────────────┘
                   │
        ┌──────────▼──────────────────┐
        │  Hiển thị trong GUI         │
        └──────────────────────────────┘
```

### Các tính năng chính

#### 1️⃣ Chọn thành phố và cập nhật dữ liệu
- Chọn thành phố từ **dropdown** ở trên cùng
- Nhấn nút **"🔄 Cập Nhật Dữ Liệu"**
- Hệ thống sẽ:
  - Kết nối API OpenWeatherMap
  - Lấy dữ liệu thời tiết 5 ngày cho thành phố đã chọn
  - Lưu file CSV thô (theo tên thành phố)
  - Xử lý & làm sạch dữ liệu
  - Vẽ tất cả biểu đồ
  - Hiển thị kết quả

#### 2️⃣ Xem biểu đồ
**Tab 1: Biểu Đồ Chính**
- Biểu đồ nhiệt độ & độ ẩm
- Histogram phân bố nhiệt độ
- Biểu đồ tốc gió

**Tab 2: Biểu Đồ Nâng Cao**
- Biểu đồ áp suất (riêng biệt với đường trung bình)
- Biểu đồ tầm nhìn (với màu sắc phân loại chất lượng)
- Biểu đồ độ che phủ mây

**Tab 3: So Sánh Thành Phố**
- So sánh nhiều thành phố cùng lúc
- Boxplot phân bố
- Nhập: `Hà Nội, TP. Hồ Chí Minh, Đà Nẵng`

**Tab 4: Thống Kê**
- Thống kê chi tiết cho thành phố đã chọn
- Bấm "🔄 Làm Mới Thống Kê" để cập nhật

#### 3️⃣ Xem dữ liệu
- File CSV thô: `data/raw/weather_raw_[TênThànhPhố].csv`
- File CSV đã xử lý: `data/processed/weather_clean_[TênThànhPhố].csv`

---

## 🔧 6. Công nghệ & Thư viện sử dụng

| Thư viện | Phiên bản | Công dụng |
|---------|---------|---------|
| **requests** | ≥2.28.0 | Gửi HTTP request tới API |
| **pandas** | ≥1.5.0 | Xử lý & phân tích dữ liệu |
| **matplotlib** | ≥3.6.0 | Vẽ biểu đồ & trực quan hóa |
| **numpy** | ≥1.23.0 | Tính toán số học |
| **seaborn** | ≥0.12.0 | Vẽ heatmap và biểu đồ nâng cao |
| **Pillow** | ≥9.0.0 | Xử lý ảnh trong GUI |
| **tkinter** | Built-in | Tạo giao diện GUI |

---

## 📊 7. Kết quả & Ví dụ đầu ra

### Dữ liệu mẫu
```
Thời Gian           Nhiệt Độ  Độ Ẩm  Áp Suất  Tốc Gió  Mô Tả
2025-12-27 12:00       24.5    65      1013     3.2    Partly cloudy
2025-12-27 15:00       25.1    63      1012     3.8    Few clouds
2025-12-27 18:00       23.2    70      1014     2.9    Rainy
```

### Biểu đồ
- ✅ Biểu đồ kết hợp (Nhiệt độ & Độ ẩm)
- ✅ Histogram phân bố nhiệt độ
- ✅ Biểu đồ tốc gió
- ✅ Biểu đồ áp suất (riêng biệt)
- ✅ Biểu đồ tầm nhìn (riêng biệt với màu sắc phân loại)
- ✅ Biểu đồ độ che phủ mây

### Phân tích thống kê
- ✅ Nhiệt độ trung bình, cao nhất, thấp nhất
- ✅ Độ ẩm trung bình
- ✅ Xu hướng (tăng/giảm)
- ✅ Độ lệch chuẩn

---

## ⚠️ 8. Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|---------|
| `401 Unauthorized` | API Key sai | Kiểm tra lại API Key, đảm bảo cấu hình đúng |
| `Connection Error` | Không có Internet | Kiểm tra kết nối mạng |
| `FileNotFoundError` | File CSV không tồn tại | Chạy "Cập nhật dữ liệu" trước |
| `ModuleNotFoundError` | Thư viện thiếu | Chạy `pip install -r requirements.txt` |
| `Empty DataFrame` | Dữ liệu không hợp lệ | Kiểm tra tên thành phố, API Key |

---

## 📝 9. Tính năng mới trong v3.0

- ✅ Hỗ trợ 11 thành phố Việt Nam
- ✅ So sánh nhiều thành phố cùng lúc  
- ✅ Biểu đồ áp suất và tầm nhìn riêng biệt, dễ hiểu hơn
- ✅ Giao diện đơn giản hóa, tập trung vào biểu đồ quan trọng
- ✅ Dữ liệu phong phú hơn (feels_like, visibility, clouds, wind_deg)
- ✅ Giao diện tabbed interface hiện đại
- ✅ Lưu trữ dữ liệu riêng biệt cho mỗi thành phố
- ✅ Fix lỗi threading khi cập nhật nhiều thành phố

## 📝 10. Phát triển tiếp theo

- [ ] Thêm dự báo dài hạn (14 ngày)
- [ ] Lưu lịch sử dữ liệu dài hạn
- [ ] Thông báo cảnh báo thời tiết nguy hiểm
- [ ] Xuất báo cáo PDF
- [ ] Đồng bộ dữ liệu với cơ sở dữ liệu
- [ ] Ứng dụng web (Flask/Django)
- [ ] Ứng dụng mobile

---

## 👥 11. Thông tin đóng góp

**Tác giả:** Nhóm [Tên nhóm]  
**Ngày tạo:** 2025-12-27  
**Trường:** [Trường đại học]  
**Môn học:** Lập trình Python (IPPA233277)

---

## 📄 12. Giấy phép

Dự án này được phát hành dưới giấy phép **MIT License**.

---

## 📞 13. Liên hệ hỗ trợ

- 📧 Email: [Email của nhóm]
- 🐙 GitHub: [Link GitHub]
- 💬 Issues: [Link Issues trên GitHub]

---

**Cảm ơn bạn đã sử dụng dự án này! 🙏**
