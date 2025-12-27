# 🧪 HƯỚNG DẪN TESTING - Testing Guide

Hướng dẫn chi tiết để kiểm tra các chức năng của dự án Weather Forecast Pro.

---

## 🎯 Chiến lược Test

### Loại Test

```
Unit Tests          → Test hàm riêng lẻ
↓
Integration Tests   → Test tương tác giữa modules
↓
System Tests        → Test toàn bộ quy trình
↓
User Acceptance Tests (UAT) → Test GUI & Trải nghiệm người dùng
```

---

## 🛠️ Chuẩn bị Testing Environment

### 1. Cài đặt Test Dependencies
```bash
# Kích hoạt virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Cài đặt thêm dev packages
pip install pytest pytest-cov black flake8 mypy
```

### 2. Cấu hình pytest
```bash
# Tạo file pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## 📋 Test Plan Chi tiết

### PHASE 1: Unit Tests

#### 1. Test data_loader.py
```python
# tests/test_data_loader.py

import pytest
import pandas as pd
from src.data_loader import fetch_weather_data

class TestDataLoader:
    """Test module lấy dữ liệu từ API"""
    
    def test_fetch_returns_dataframe(self):
        """✅ Test: fetch_weather_data trả về DataFrame"""
        df = fetch_weather_data()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    
    def test_fetch_has_required_columns(self):
        """✅ Test: DataFrame có tất cả cột cần thiết"""
        df = fetch_weather_data()
        required = ['dt_txt', 'temp', 'humidity', 'pressure', 'wind_speed', 'description']
        assert all(col in df.columns for col in required)
    
    def test_fetch_dataframe_not_empty(self):
        """✅ Test: DataFrame không trống"""
        df = fetch_weather_data()
        assert len(df) > 0
        assert len(df) >= 40  # Ít nhất 40 bản ghi (5 ngày × 8 mốc)
    
    def test_temperature_in_valid_range(self):
        """✅ Test: Nhiệt độ trong phạm vi hợp lý"""
        df = fetch_weather_data()
        assert (df['temp'] >= -100).all()
        assert (df['temp'] <= 70).all()
    
    def test_humidity_in_valid_range(self):
        """✅ Test: Độ ẩm 0-100%"""
        df = fetch_weather_data()
        assert (df['humidity'] >= 0).all()
        assert (df['humidity'] <= 100).all()
    
    def test_wind_speed_positive(self):
        """✅ Test: Tốc gió không âm"""
        df = fetch_weather_data()
        assert (df['wind_speed'] >= 0).all()
    
    def test_no_duplicate_datetime(self):
        """✅ Test: Không có thời gian trùng lặp"""
        df = fetch_weather_data()
        assert not df['dt_txt'].duplicated().any()
    
    def test_invalid_api_key(self):
        """✅ Test: API Key sai → Trả về None"""
        # Tạo API Key sai
        import src.config as config
        old_key = config.API_KEY
        config.API_KEY = "INVALID_KEY_123456"
        
        df = fetch_weather_data()
        assert df is None  # Hoặc exception
        
        config.API_KEY = old_key  # Restore
```

#### 2. Test data_cleaner.py
```python
# tests/test_data_cleaner.py

import pandas as pd
from src.data_cleaner import clean_data

class TestDataCleaner:
    """Test module làm sạch dữ liệu"""
    
    def test_clean_returns_dataframe(self):
        """✅ Test: clean_data trả về DataFrame"""
        df = clean_data()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    
    def test_clean_has_vietnamese_columns(self):
        """✅ Test: Các cột được đổi sang Tiếng Việt"""
        df = clean_data()
        expected = ['Thời Gian', 'Nhiệt Độ', 'Độ Ẩm', 'Áp Suất', 'Tốc Gió', 'Mô Tả']
        assert list(df.columns) == expected
    
    def test_clean_datetime_converted(self):
        """✅ Test: Thời gian được chuyển sang DateTime"""
        df = clean_data()
        assert pd.api.types.is_datetime64_any_dtype(df['Thời Gian'])
    
    def test_clean_no_null_values(self):
        """✅ Test: Không có giá trị null"""
        df = clean_data()
        assert df.isnull().sum().sum() == 0
    
    def test_clean_no_duplicates(self):
        """✅ Test: Không có dòng trùng lặp"""
        df = clean_data()
        assert not df.duplicated(subset=['Thời Gian']).any()
    
    def test_clean_temperature_rounded(self):
        """✅ Test: Nhiệt độ được làm tròn 1 chữ số"""
        df = clean_data()
        # Kiểm tra chỉ có 1 chữ số thập phân
        assert all(str(x).split('.')[-1].__len__() <= 1 for x in df['Nhiệt Độ'])
    
    def test_clean_humidity_is_integer(self):
        """✅ Test: Độ ẩm là số nguyên"""
        df = clean_data()
        assert df['Độ Ẩm'].dtype in ['int64', 'int32']
    
    def test_clean_removes_outliers(self):
        """✅ Test: Outlier được loại bỏ"""
        df = clean_data()
        assert (df['Nhiệt Độ'] >= -100).all()
        assert (df['Nhiệt Độ'] <= 70).all()
```

#### 3. Test statistics.py
```python
# tests/test_statistics.py

import pandas as pd
from src.statistics import calculate_statistics, analyze_trend, get_weather_summary

class TestStatistics:
    """Test module thống kê"""
    
    def test_calculate_statistics_returns_dict(self):
        """✅ Test: calculate_statistics trả về dict"""
        from src.data_cleaner import clean_data
        df = clean_data()
        stats = calculate_statistics(df)
        assert isinstance(stats, dict)
        assert 'Nhiệt Độ' in stats
    
    def test_statistics_has_required_keys(self):
        """✅ Test: Thống kê có tất cả chỉ số"""
        from src.data_cleaner import clean_data
        df = clean_data()
        stats = calculate_statistics(df)
        required_keys = ['mean', 'min', 'max', 'std', 'median']
        assert all(key in stats['Nhiệt Độ'] for key in required_keys)
    
    def test_analyze_trend_returns_dict(self):
        """✅ Test: analyze_trend trả về dict"""
        from src.data_cleaner import clean_data
        df = clean_data()
        trends = analyze_trend(df)
        assert isinstance(trends, dict)
        assert 'Nhiệt Độ' in trends
    
    def test_get_weather_summary_complete(self):
        """✅ Test: Tóm tắt đầy đủ"""
        from src.data_cleaner import clean_data
        df = clean_data()
        summary = get_weather_summary(df)
        assert 'Thời gian' in summary
        assert 'Nhiệt độ' in summary
        assert 'Độ ẩm' in summary
```

#### 4. Test visualizer.py
```python
# tests/test_visualizer.py

import os
from src.visualizer import create_weather_chart, create_temperature_histogram, create_wind_speed_chart
from src.config import CHART_PATH

class TestVisualizer:
    """Test module vẽ biểu đồ"""
    
    def test_create_weather_chart_returns_path(self):
        """✅ Test: create_weather_chart trả về đường dẫn file"""
        path = create_weather_chart()
        assert path is not None
        assert isinstance(path, str)
    
    def test_create_weather_chart_file_exists(self):
        """✅ Test: File biểu đồ được tạo"""
        path = create_weather_chart()
        assert os.path.exists(path)
    
    def test_chart_file_is_png(self):
        """✅ Test: File là PNG"""
        path = create_weather_chart()
        assert path.endswith('.png')
    
    def test_create_histogram_creates_file(self):
        """✅ Test: Histogram được tạo"""
        path = create_temperature_histogram()
        assert path is not None
        assert os.path.exists(path)
    
    def test_create_wind_chart_creates_file(self):
        """✅ Test: Biểu đồ tốc gió được tạo"""
        path = create_wind_speed_chart()
        assert path is not None
        assert os.path.exists(path)
```

---

### PHASE 2: Integration Tests

```python
# tests/test_integration.py

import pandas as pd
from src.data_loader import fetch_weather_data
from src.data_cleaner import clean_data
from src.visualizer import create_all_charts
from src.statistics import calculate_statistics

class TestIntegration:
    """Test tương tác giữa các modules"""
    
    def test_full_pipeline(self):
        """✅ Test: Quy trình đầy đủ API → Clean → Visualize"""
        # 1. Lấy dữ liệu
        df_raw = fetch_weather_data()
        assert df_raw is not None
        
        # 2. Làm sạch
        df_clean = clean_data()
        assert len(df_clean) <= len(df_raw)  # Số bản ghi không tăng
        
        # 3. Vẽ biểu đồ
        success = create_all_charts()
        assert success == True
        
        # 4. Tính thống kê
        stats = calculate_statistics(df_clean)
        assert len(stats) > 0
    
    def test_data_consistency(self):
        """✅ Test: Dữ liệu nhất quán giữa các module"""
        df_clean = clean_data()
        stats = calculate_statistics(df_clean)
        
        # Kiểm tra mean từ stats == tính toán
        assert abs(stats['Nhiệt Độ']['mean'] - df_clean['Nhiệt Độ'].mean()) < 0.01
    
    def test_error_handling_chain(self):
        """✅ Test: Xử lý lỗi truyền cascade"""
        # Nếu API fail, code không crash
        df_raw = fetch_weather_data()
        
        if df_raw is None:
            df_clean = clean_data()
            # Cũng phải fail gracefully
            assert df_clean is None or isinstance(df_clean, pd.DataFrame)
```

---

### PHASE 3: User Acceptance Tests (UAT)

#### Test Checklist
```
[ ] GUI khởi động không lỗi
[ ] Nút "Cập nhật" hoạt động
[ ] Nút "Thống kê" hoạt động
[ ] Biểu đồ hiển thị chính xác
[ ] Thông báo lỗi rõ ràng
[ ] Biểu đồ resize phù hợp
[ ] Không có delay >= 5 giây
```

#### Test Case 1: API Success
```
Tiên quyết: API Key hợp lệ
Bước:
1. Khởi động ứng dụng
2. Bấm "Cập nhật Dữ Liệu"
3. Chờ thông báo

Kỳ vọng:
✅ Thông báo "Thành công"
✅ Biểu đồ hiển thị
✅ Trạng thái: xanh (OK)
```

#### Test Case 2: API Key Sai
```
Tiên quyết: API Key sai (INVALID_KEY)
Bước:
1. Khởi động ứng dụng
2. Bấm "Cập nhật Dữ Liệu"
3. Chờ thông báo

Kỳ vọng:
✅ Thông báo lỗi xuất hiện
✅ Hướng dẫn kiểm tra API Key
✅ Trạng thái: đỏ (ERROR)
```

#### Test Case 3: Thành Phố Không Tồn Tại
```
Tiên quyết: CITY_NAME = "Thành phố không có"
Bước:
1. Khởi động ứng dụng
2. Bấm "Cập nhật Dữ Liệu"

Kỳ vọng:
✅ Thông báo lỗi 404
✅ Hướng dẫn kiểm tra tên thành phố
```

#### Test Case 4: Không Có Internet
```
Tiên quyết: Tắt kết nối mạng
Bước:
1. Khởi động ứng dụng
2. Bấm "Cập nhật Dữ Liệu"

Kỳ vọng:
✅ Thông báo lỗi kết nối
✅ Không crash
```

---

## 🚀 Chạy Tests

### 1. Chạy tất cả tests
```bash
pytest tests/ -v
```

### 2. Chạy test cụ thể
```bash
# Test file
pytest tests/test_data_loader.py -v

# Test class
pytest tests/test_data_loader.py::TestDataLoader -v

# Test function
pytest tests/test_data_loader.py::TestDataLoader::test_fetch_returns_dataframe -v
```

### 3. Chạy với coverage
```bash
pytest tests/ --cov=src/ --cov-report=html
# Xem report: htmlcov/index.html
```

### 4. Chạy nhanh (skip slow tests)
```bash
pytest tests/ -m "not slow" -v
```

---

## 📊 Coverage Target

```
Target: >= 80% code coverage

Module           Target   Current
─────────────────────────────────
data_loader.py   85%      ?
data_cleaner.py  85%      ?
visualizer.py    80%      ?
statistics.py    85%      ?
config.py        90%      ?
main.py          70%      ? (GUI hard to test)
─────────────────────────────────
TOTAL            80%      ?
```

---

## 🐛 Test Troubleshooting

### Lỗi 1: ModuleNotFoundError: No module named 'src'
**Giải pháp:**
```bash
# Chạy từ root directory
cd Weather_Forecast_Pro
pytest tests/
```

### Lỗi 2: API request failed
**Giải pháp:**
```python
# Mock API response
import pytest
from unittest.mock import patch

@patch('src.data_loader.requests.get')
def test_with_mock_api(mock_get):
    mock_get.return_value.json.return_value = {...}
    ...
```

### Lỗi 3: File not found (weather_clean.csv)
**Giải pháp:**
```python
# Tạo fixture
@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    fetch_weather_data()
    clean_data()
    yield
```

---

## ✅ Test Results Template

```
======= test session starts =========
platform win32 -- Python 3.9.0, pytest-7.x.x
rootdir: /Weather_Forecast_Pro
collected 20 items

tests/test_data_loader.py PASSED         [5%]
tests/test_data_cleaner.py PASSED        [25%]
tests/test_statistics.py PASSED          [45%]
tests/test_visualizer.py PASSED          [65%]
tests/test_integration.py PASSED         [85%]

======= 20 passed in 12.34s =========

Coverage: 82%
```

---

## 📚 Tài liệu thêm

- 📖 [pytest Documentation](https://docs.pytest.org/)
- 🔗 [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- 📊 [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

**Cập nhật cuối:** 2025-12-27
