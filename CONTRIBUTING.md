# 🤝 HƯỚNG DẪN ĐÓNG GÓP (CONTRIBUTING)

Cảm ơn bạn quan tâm đến dự án **Weather Forecast Pro**! Chúng tôi hoan nghênh các đóng góp từ cộng đồng.

---

## 📋 Quy tắc chung

1. **Tôn trọng** tất cả các thành viên trong cộng đồng
2. **Ghi rõ** lý do khi tạo Issue hoặc Pull Request
3. **Kiểm tra** xem Issue/PR tương tự đã tồn tại chưa
4. **Tuân thủ** Style Guide của dự án

---

## 🐛 Báo cáo Lỗi (Bug Reports)

### Cách báo cáo lỗi

1. **Tìm kiếm** xem lỗi đã được báo cáo chưa
2. **Mô tả chi tiết:**
   - Lỗi là gì?
   - Cách tái hiện lỗi?
   - Kết quả mong đợi vs kết quả thực tế
   - Phiên bản Python, OS, các package

3. **Ví dụ Issue tốt:**
```markdown
## 🐛 Lỗi: Ứng dụng crash khi cập nhật dữ liệu

### Mô tả
Ứng dụng bị crash khi bấm nút "Cập Nhật Dữ Liệu"

### Cách tái hiện
1. Khởi động ứng dụng
2. Bấm nút "Cập Nhật Dữ Liệu Mới Nhất"
3. Chờ vài giây → Ứng dụng crash

### Lỗi
```
Traceback (most recent call last):
  File "src/data_loader.py", line 45, in fetch_weather_data
    response.raise_for_status()
requests.exceptions.HTTPError: 401 Client Error
```

### Thông tin hệ thống
- **Python:** 3.9.0
- **OS:** Windows 10
- **API Key:** Đã kiểm tra và hợp lệ
```

---

## 💡 Đề xuất Tính năng (Feature Requests)

### Cách đề xuất tính năng mới

1. **Kiểm tra** xem tính năng đã tồn tại chưa
2. **Giải thích:**
   - Tính năng là gì?
   - Tại sao cần nó?
   - Ví dụ sử dụng
3. **Lưu ý:** Không spam hoặc đề xuất quá liều lĩnh

### Ví dụ đề xuất tốt:
```markdown
## ✨ Tính năng: Dự báo dài hạn 14 ngày

### Mô tả
Thêm hỗ trợ dự báo 14 ngày thay vì chỉ 5 ngày hiện tại

### Lợi ích
- Giúp người dùng lên kế hoạch dài hạn tốt hơn
- Phổ biến trên các ứng dụng thời tiết khác

### Cách thực hiện
Sử dụng endpoint `/forecast/cli` của OpenWeatherMap (yêu cầu API Pro)
```

---

## 🔧 Hướng dẫn Phát triển

### 1. Fork & Clone
```bash
# Fork dự án trên GitHub
# Clone fork của bạn
git clone https://github.com/YOUR_USERNAME/Weather_Forecast_Pro.git
cd Weather_Forecast_Pro
```

### 2. Tạo Branch
```bash
# Tạo branch mới cho tính năng/lỗi
git checkout -b feature/tên-tính-năng
# hoặc
git checkout -b bugfix/mô-tả-lỗi
```

### 3. Cài đặt Environment
```bash
# Tạo môi trường ảo
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt

# Cài thêm dev dependencies
pip install pytest black flake8
```

### 4. Phát triển
```bash
# Viết code của bạn
# Kiểm tra syntax
python -m flake8 src/

# Format code
python -m black src/

# Chạy tests (nếu có)
pytest tests/
```

### 5. Commit & Push
```bash
# Kiểm tra thay đổi
git status

# Thêm files
git add .

# Commit với message rõ ràng
git commit -m "Thêm tính năng XYZ" -m "Chi tiết lý do"

# Push lên fork
git push origin feature/tên-tính-năng
```

### 6. Tạo Pull Request
1. Truy cập GitHub → Fork của bạn
2. Bấm "Compare & pull request"
3. **Mô tả chi tiết:**
   - Tính năng/lỗi là gì?
   - Thay đổi gì?
   - Có breaking changes không?
4. Bấm "Create pull request"

---

## 📝 Style Guide

### Naming Convention
```python
# ✅ Tốt
def fetch_weather_data():
    pass

class WeatherApp:
    pass

CITY_NAME = "Hanoi"
my_variable = 42

# ❌ Xấu
def FetchWeatherData():  # CamelCase cho function
    pass

myVariable = 42  # camelCase cho biến toàn cục
```

### Docstring
```python
def calculate_average(data: list) -> float:
    """
    Tính trung bình cộng của dữ liệu.
    
    Args:
        data: Danh sách số liệu
        
    Returns:
        float: Giá trị trung bình
        
    Raises:
        ValueError: Nếu dữ liệu rỗng
        
    Example:
        >>> calculate_average([1, 2, 3])
        2.0
    """
    pass
```

### Type Hints
```python
from typing import Optional, List, Dict

def process_data(values: List[float]) -> Optional[Dict[str, float]]:
    """Xử lý dữ liệu với type hints rõ ràng"""
    pass
```

### Comments
```python
# ✅ Tốt: Giải thích TẠI SAO, không phải CÁI GÌ
# Kiểm tra API Key vì nếu không có sẽ gây lỗi 401
if not api_key:
    return None

# ❌ Xấu: Comment hiển nhiên
x = 5  # Gán 5 cho x
```

---

## 🧪 Testing

### Tạo test
```python
# tests/test_data_loader.py
import pytest
from src.data_loader import fetch_weather_data

def test_fetch_returns_dataframe():
    """Test: fetch_weather_data trả về DataFrame"""
    df = fetch_weather_data()
    assert df is not None
    assert len(df) > 0

def test_fetch_required_columns():
    """Test: DataFrame có tất cả cột cần thiết"""
    df = fetch_weather_data()
    required = ['Thời Gian', 'Nhiệt Độ', 'Độ Ẩm']
    assert all(col in df.columns for col in required)
```

### Chạy test
```bash
pytest tests/ -v

# Với coverage
pytest tests/ --cov=src/
```

---

## 📚 Cấu trúc Commit Message

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Loại commit:
- **feat**: Tính năng mới
- **fix**: Sửa lỗi
- **docs**: Tài liệu
- **style**: Format, không ảnh hưởng logic
- **refactor**: Tổ chức lại code
- **test**: Thêm test
- **chore**: Cập nhật dependencies, config

### Ví dụ:
```
feat(visualizer): thêm histogram phân bố nhiệt độ

- Vẽ histogram với 10 bins
- Thêm đường Gaussian overlay
- Hiển thị mu và sigma trên đồ thị

Closes #25
```

---

## 🚀 Quy trình Review

1. **Maintainer** sẽ review PR của bạn
2. **Có thể yêu cầu** thay đổi hoặc giải thích
3. **Sau khi duyệt** sẽ merge vào main
4. **Cảm ơn** bạn đã đóng góp!

---

## ⚖️ License

Khi bạn đóng góp, bạn đồng ý rằng code của bạn sẽ được phát hành dưới giấy phép **MIT**.

---

## 📞 Cần giúp?

- 📧 Email: [Email nhóm]
- 💬 Discussions: [Link discussions]
- 🐛 Issues: [Link issues]

**Cảm ơn bạn! 🙏**
