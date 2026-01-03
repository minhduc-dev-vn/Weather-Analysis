# 📄 MÔ TẢ CHI TIẾT DỮ LIỆU DỰ ÁN (Detailed Data Description)

Tài liệu này cung cấp cái nhìn toàn diện về tập dữ liệu được sử dụng trong hệ thống **Weather Forecast Pro**, bao gồm nguồn gốc, cấu trúc kỹ thuật, mục đích sử dụng và các hạn chế liên quan.

---

## 🕒 1. Lịch sử và Nguồn gốc (History & Origin)

- **Nguồn dữ liệu:** Dữ liệu được trích xuất trực tiếp từ **OpenWeatherMap API** (One Call API hoặc 5 Day / 3 Hour Forecast).
- **Lịch sử hình thành:** Tập dữ liệu được thu thập bắt đầu từ giai đoạn phát triển dự án (tháng 12/2025). Đây là dữ liệu thời gian thực (Real-time data) và dữ liệu dự báo ngắn hạn.
- **Phương pháp thu thập:** Sử dụng thư viện `requests` trong Python để gửi các truy vấn HTTP tới server của OpenWeatherMap và nhận về kết quả định dạng JSON, sau đó được chuyển đổi sang CSV để lưu trữ cục bộ.

---

## 🎯 2. Mục đích và Công dụng (Purpose & Usage)

- **Mục đích:** Cung cấp thông tin dự báo thời tiết chính xác trong vòng 5 ngày tới cho các thành phố lớn tại Việt Nam.
- **Lĩnh vực áp dụng:** Khí tượng thủy văn, Phân tích dữ liệu dữ liệu (Data Analysis), và Ứng dụng hỗ trợ đời sống dân dụng.
- **Công dụng:** 
    - Giúp người dùng lên kế hoạch sinh hoạt và làm việc dựa trên điều kiện thời tiết.
    - Phân tích xu hướng biến đổi nhiệt độ và độ ẩm trong ngắn hạn.
    - Cảnh báo các điều kiện thời tiết đặc biệt (áp suất thấp, tầm nhìn xa giảm, v.v.).

---

## 📊 3. Danh sách Đặc trưng và Kiểu dữ liệu (Features & Data Types)

Dữ liệu sau khi qua module `src/data_cleaner.py` sẽ có cấu trúc như sau:

| STT | Tên đặc trưng (Việt) | Tên gốc (Technical) | Kiểu dữ liệu | Mô tả | Đơn vị |
|:---:|:---|:---|:---:|:---|:---|
| 1 | **Thời Gian** | `dt_txt` | DateTime | Thời điểm dự báo (mỗi 3 giờ) | YYYY-MM-DD HH:MM:SS |
| 2 | **Nhiệt Độ** | `temp` | Float | Nhiệt độ không khí đo thực tế | °C |
| 3 | **Nhiệt Độ Cảm Nhận** | `feels_like` | Float | Nhiệt độ dựa trên cảm nhận con người | °C |
| 4 | **Độ Ẩm** | `humidity` | Integer | Độ ẩm tương đối của không khí | % |
| 5 | **Áp Suất** | `pressure` | Integer | Áp suất khí quyển tại mực nước biển | hPa |
| 6 | **Tốc Độ Gió** | `wind_speed` | Float | Tốc độ gió di chuyển theo phương ngang | m/s |
| 7 | **Hướng Gió** | `wind_deg` | Integer | Hướng gió thổi (theo vòng tròn 360 độ) | Độ (°) |
| 8 | **Độ Che Phủ Mây** | `clouds` | Integer | Tỷ lệ phần trăm mây che phủ bầu trời | % |
| 9 | **Tầm Nhìn** | `visibility` | Float | Khoảng cách quan sát tối đa | km |
| 10 | **Mô Tả** | `description` | String | Trạng thái thời tiết (trời quang, mưa,...) | Văn bản |
| 11 | **Thành Phố** | `city_name` | String | Tên thành phố được dự báo | Tên riêng |

---

## 🛠️ 4. Quy trình Xử lý Dữ liệu (Data Processing)

Dữ liệu không được sử dụng trực tiếp ở dạng thô mà trải qua các bước chuẩn hóa:
1.  **Làm sạch (Cleaning):** Loại bỏ các bản ghi trùng lặp (duplicates) dựa trên mốc thời gian.
2.  **Chỉnh lý (Imputation):** Điền các giá trị thiếu bằng phương pháp trung bình (mean) hoặc trung vị (median) để đảm bảo tính liên tục của biểu đồ.
3.  **Chuyển đổi (Transformation):** 
    - Tầm nhìn được đổi từ mét (m) sang kilômét (km).
    - Thời gian được chuyển về múi giờ địa phương và định dạng chuẩn Python.
4.  **Làm tròn (Rounding):** Nhiệt độ được làm tròn đến 1 chữ số thập phân, các đại lượng phần trăm được chuyển về số nguyên.

---

## ⚠️ 5. Hạn chế và Khiếm khuyết (Limitations & Defects)

Mặc dù dữ liệu được lấy từ nguồn uy tín, hệ thống vẫn tồn tại một số hạn chế:

- **Hạn chế kỹ thuật:**
    - **API Rate Limit:** Gói miễn phí giới hạn số lượng request, dẫn đến việc dữ liệu không thể cập nhật liên tục từng giây.
    - **Phu thuộc Internet:** Hệ thống không thể lấy dữ liệu mới nếu mất kết nối mạng.
- **Khiếm khuyết dữ liệu:**
    - **Độ chính xác:** Dữ liệu dự báo có độ sai lệch tăng dần theo thời gian (dự báo ngày thứ 5 sẽ kém chính xác hơn ngày thứ 1).
    - **Phạm vi địa lý:** OpenWeatherMap đôi khi không có dữ liệu chi tiết cho các khu vực vùng sâu vùng xa hoặc thành phố quá nhỏ.
    - **Dữ liệu lịch sử:** Phiên bản hiện tại tập trung vào dự báo tương lai, chưa lưu trữ cơ sở dữ liệu lịch sử dài hạn (nhiều năm).

---

## 🌍 6. Phạm vi Thành phố hỗ trợ

Dữ liệu hiện được lấy cho 11 địa điểm tiêu biểu:
*Hà Nội, TP. Hồ Chí Minh, Đà Nẵng, Cần Thơ, Nha Trang, Huế, Quy Nhơn, Phan Thiết, Đà Lạt, Hạ Long, Vũng Tàu.*

---
*Tài liệu được cập nhật tự động bởi hệ thống Weather Forecast Pro.*
