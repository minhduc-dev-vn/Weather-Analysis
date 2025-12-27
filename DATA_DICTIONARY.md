# 📊 DATA DICTIONARY - Mô Tả Chi Tiết Dữ Liệu

## 1. Tổng quan dữ liệu

### Thông tin chung
| Thuộc tính | Giá trị |
|-----------|--------|
| **Tên dataset** | OpenWeatherMap Weather Forecast Data |
| **Nguồn** | OpenWeatherMap API (https://openweathermap.org) |
| **Loại dữ liệu** | Dự báo thời tiết 5 ngày |
| **Tần suất cập nhật** | 3 giờ/lần |
| **Định dạng gốc** | JSON |
| **Định dạng xử lý** | CSV (UTF-8) |
| **Số lượng bản ghi** | ~40 bản ghi (5 ngày × 8 mốc/ngày) |
| **Số lượng cột** | 6 cột chính |
| **Kích thước file** | ~10-20 KB |

---

## 2. Chi tiết từng cột dữ liệu

### 🕐 Cột 1: `dt_txt` (Thời Gian)

**Tên tiếng Việt:** Thời Gian  
**Kiểu dữ liệu:** DateTime (YYYY-MM-DD HH:MM:SS)  
**Nguồn:** Trường `dt_txt` từ API

**Mô tả:**
- Mốc thời gian dự báo
- Cập nhật mỗi 3 giờ
- Theo múi giờ UTC (có thể chuyển đổi sau)

**Ví dụ giá trị:**
```
2025-12-27 12:00:00
2025-12-27 15:00:00
2025-12-28 00:00:00
```

**Phạm vi giá trị:**
- Từ thời điểm hiện tại đến 5 ngày trong tương lai
- Không có giá trị null

**Kiểm tra chất lượng:**
- ✅ Không có giá trị trùng lặp (mỗi mốc thời gian có 1 bản ghi)
- ✅ Sắp xếp theo thứ tự tăng dần
- ✅ Không có giá trị thiếu

---

### 🌡️ Cột 2: `temp` (Nhiệt Độ)

**Tên tiếng Việt:** Nhiệt Độ  
**Kiểu dữ liệu:** Float (thực số)  
**Đơn vị:** °C (Celsius)  
**Nguồn:** Trường `main.temp` từ API

**Mô tả:**
- Nhiệt độ không khí tại vị trí dự báo
- Được cập nhật từ các trạm khí tượng

**Phạm vi giá trị:**
- Tối thiểu: -50°C
- Tối đa: +55°C
- Phạm vi thông thường: 15-35°C (tùy vào mùa và vị trí)

**Ví dụ giá trị:**
```
24.5 °C
25.1 °C
23.2 °C
```

**Kiểm tra chất lượng:**
- ✅ Không có giá trị null
- ⚠️ Kiểm tra outlier: nếu < -50 hoặc > 55, đánh dấu
- ✅ Làm tròn 1 chữ số sau dấu phẩy

**Xử lý trong code:**
```python
df['temp'].round(1)  # Làm tròn 1 chữ số
```

---

### 💧 Cột 3: `humidity` (Độ Ẩm)

**Tên tiếng Việt:** Độ Ẩm  
**Kiểu dữ liệu:** Integer (số nguyên)  
**Đơn vị:** % (phần trăm)  
**Nguồn:** Trường `main.humidity` từ API

**Mô tả:**
- Độ ẩm tương đối của không khí
- Thể hiện lượng hơi nước trong không khí

**Phạm vi giá trị:**
- Tối thiểu: 0%
- Tối đa: 100%

**Ví dụ giá trị:**
```
65 %
63 %
70 %
```

**Kiểm tra chất lượng:**
- ✅ Không có giá trị null
- ✅ Luôn trong khoảng 0-100
- ✅ Không cần làm tròn (đã là số nguyên)

**Mối quan hệ:**
- Độ ẩm cao thường kèm theo mưa hoặc sương mù
- Độ ẩm thấp thường là thời tiết nắng

---

### 🌪️ Cột 4: `pressure` (Áp Suất)

**Tên tiếng Việt:** Áp Suất  
**Kiểu dữ liệu:** Integer  
**Đơn vị:** hPa (hectoPascal)  
**Nguồn:** Trường `main.pressure` từ API

**Mô tả:**
- Áp suất khí quyển tại mực nước biển
- Dùng để dự báo thay đổi thời tiết

**Phạm vi giá trị:**
- Tối thiểu: 870 hPa
- Tối đa: 1050 hPa
- Giá trị bình thường: 1010-1020 hPa

**Ví dụ giá trị:**
```
1013 hPa
1012 hPa
1014 hPa
```

**Kiểm tra chất lượng:**
- ✅ Không có giá trị null
- ⚠️ Kiểm tra outlier: nếu < 870 hoặc > 1050
- ✅ Không cần làm tròn

**Ý nghĩa:**
- **Áp suất cao (> 1020):** Thời tiết ổn định, nắng
- **Áp suất thấp (< 1000):** Có thể có mưa, bão

---

### 💨 Cột 5: `wind_speed` (Tốc Gió)

**Tên tiếng Việt:** Tốc Gió  
**Kiểu dữ liệu:** Float  
**Đơn vị:** m/s (mét/giây)  
**Nguồn:** Trường `wind.speed` từ API

**Mô tả:**
- Tốc độ gió ngang (không tính phương hướng)
- Ảnh hưởng đến cảm giác nhiệt độ thực

**Phạm vi giá trị:**
- Tối thiểu: 0 m/s
- Tối đa: 20+ m/s

**Ví dụ giá trị:**
```
3.2 m/s
3.8 m/s
2.9 m/s
```

**Chuyển đổi đơn vị:**
- **Sang km/h:** m/s × 3.6 = km/h
- **Sang knots:** m/s × 1.944 = knots

**Kiểm tra chất lượng:**
- ✅ Không có giá trị null
- ⚠️ Kiểm tra outlier: nếu > 30 m/s
- ✅ Làm tròn 2 chữ số sau dấu phẩy

**Mức độ gió Beaufort:**
| m/s | Tốc độ | Mô tả |
|-----|--------|-------|
| 0-0.5 | 0-2 km/h | Yên tĩnh |
| 0.5-2 | 2-7 km/h | Nhẹ |
| 2-5 | 7-18 km/h | Vừa |
| 5-10 | 18-36 km/h | Mạnh |
| >10 | >36 km/h | Rất mạnh |

---

### ☁️ Cột 6: `description` (Mô Tả)

**Tên tiếng Việt:** Mô Tả  
**Kiểu dữ liệu:** String (văn bản)  
**Nguồn:** Trường `weather[0].description` từ API

**Mô tả:**
- Mô tả tóm tắt điều kiện thời tiết
- Văn bản tiếng Việt từ API

**Giá trị có thể:**
```
Partly cloudy      (Mây rải rác)
Few clouds         (Ít mây)
Rainy              (Mưa)
Clear sky          (Trời quang)
Cloudy             (Mây)
Thunderstorm       (Bão sét)
Foggy              (Sương mù)
```

**Kiểm tra chất lượng:**
- ✅ Không có giá trị null
- ✅ Không có khoảng trắng thừa
- ✅ Đã được normalize (chữ thường)

---

## 3. Chất lượng dữ liệu

### Tổng kết kiểm tra

| Vấn đề | Trạng thái | Xử lý |
|--------|-----------|------|
| **Giá trị null** | ✅ Không có | Không cần xử lý |
| **Giá trị trùng** | ✅ Không có | Không cần xử lý |
| **Định dạng sai** | ⚠️ Có thể (thời gian) | Chuyển sang DateTime |
| **Outlier** | ⚠️ Hiếm | Kiểm tra & đánh dấu |
| **Dữ liệu thiếu** | ⚠️ Có thể (tên thành phố) | In cảnh báo |

### Quy trình làm sạch dữ liệu

```python
# 1. Chuyển đổi thời gian
df['Thời Gian'] = pd.to_datetime(df['dt_txt'])

# 2. Làm tròn số liệu
df['Nhiệt Độ'] = df['temp'].round(1)
df['Tốc Gió'] = df['wind_speed'].round(2)

# 3. Kiểm tra outlier
df = df[df['Nhiệt Độ'] > -50]  # Loại bỏ nhiệt độ không hợp lý

# 4. Đổi tên cột
df = df.rename(columns={'temp': 'Nhiệt Độ', ...})

# 5. Lưu file
df.to_csv('weather_clean.csv', index=False)
```

---

## 4. Mối quan hệ giữa các cột

### Biểu đồ mối quan hệ

```
Thời Gian (dt_txt)
    ↓
┌───┴───────┬──────────┬──────────┬─────────┐
↓           ↓          ↓          ↓         ↓
Nhiệt Độ   Độ Ẩm   Áp Suất   Tốc Gió  Mô Tả
(temp)   (humidity)(pressure)(wind_speed)(description)
```

### Các mối quan hệ quan trọng

1. **Nhiệt độ ↔ Độ ẩm**
   - Tương quan nghịch: Nhiệt độ cao → Độ ẩm thấp
   - Ví dụ: Ngày nắng (25°C) thường có độ ẩm 40-60%

2. **Áp suất ↔ Mô tả**
   - Áp suất thấp → Thường có mưa
   - Áp suất cao → Thường là trời quang

3. **Tốc gió ↔ Mô tả**
   - Tốc gió cao → Bão, dông
   - Tốc gió thấp → Yên tĩnh, không mưa

---

## 5. Hạn chế dữ liệu

### Những điểm cần lưu ý

❌ **API Key phải hoạt động**
- Cần đăng ký tài khoản OpenWeatherMap
- API Key hoạt động sau vài phút đến vài giờ

❌ **Phụ thuộc mạng**
- Không có Internet → Không lấy được dữ liệu mới
- Phải dùng dữ liệu cache cũ

❌ **Giới hạn API**
- Gói miễn phí: 60 lần gọi/phút
- Không thể cập nhật quá sớm

⚠️ **Độ chính xác**
- Dự báo chỉ chính xác 5 ngày
- Dự báo xa (4-5 ngày) ít chính xác hơn

⚠️ **Thành phố nhỏ**
- Một số thành phố/xã nhỏ có dữ liệu không chính xác
- Nên dùng tên thành phố chính

⚠️ **Múi giờ**
- API trả về giờ UTC
- Cần chuyển đổi thành giờ địa phương

---

## 6. Cách sử dụng dữ liệu

### Ứng dụng thực tế

- 📊 **Phân tích xu hướng:** Xem thời tiết sẽ nóng hay lạnh
- 📈 **Dự báo:** Chuẩn bị cho thời tiết xấu
- 🎯 **So sánh:** So sánh thời tiết giữa các ngày
- 🧪 **Nghiên cứu:** Học các mô hình dự báo thời tiết

---

## 7. Liên kết tham khảo

- 📚 [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- 📖 [Pandas Documentation](https://pandas.pydata.org/docs/)
- 🎨 [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

**Cập nhật lần cuối:** 2025-12-27
