# 📋 PHÂN CÔNG CÔNG VIỆC - WORK DISTRIBUTION

**Dự Án:** Hệ Thống Phân Tích và Dự Báo Thời Tiết (Weather Forecast Pro)  
**Môn Học:** Lập Trình Python (IPPA233277)  
**Thời Gian:** 2025-12-20 → 2025-12-27 (8 ngày)  
**Nhóm:** [Tên Nhóm]

---

## 👥 Thành viên nhóm

| STT | Tên | MSSV | Vai trò | Công việc chính |
|-----|-----|------|---------|-----------------|
| 1 | [Tên thành viên 1] | [Mã] | **Team Lead** | Quản lý dự án, Backend chính |
| 2 | [Tên thành viên 2] | [Mã] | **Dev Backend** | Xử lý dữ liệu, Thống kê |
| 3 | [Tên thành viên 3] | [Mã] | **Dev Frontend** | Giao diện GUI, Trực quan hóa |
| 4 | [Tên thành viên 4] | [Mã] | **QA / Tài liệu** | Test, Viết README, tài liệu |
| 5 | [Tên thành viên 5] | [Mã] | **DevOps** | GitHub, Deploy, CI/CD (tuỳ chọn) |

---

## 📌 Phân công chi tiết

### 🎯 Phase 1: Thiết kế & Chuẩn bị (2025-12-20 ~ 2025-12-21)

#### Thành viên 1 (Team Lead)
- ✅ **Tổng kết yêu cầu đề tài**
  - [x] Đọc kỹ đề bài
  - [x] Xác định scope công việc
  - [x] Lập kế hoạch timeline
  - **Kết quả:** Chuyên đề 8 ngày rõ ràng

- ✅ **Thiết kế kiến trúc**
  - [x] Vẽ sơ đồ cấu trúc dự án
  - [x] Định nghĩa các module
  - **Kết quả:** Cấu trúc thư mục rõ ràng

#### Thành viên 4 (QA / Tài liệu)
- ✅ **Thiết lập Git Repository**
  - [x] Tạo repo GitHub/GitLab
  - [x] Cấu hình .gitignore
  - [x] Tạo branch chính (main, develop)
  - **Kết quả:** GitHub sẵn sàng

- ✅ **Chuẩn bị tài liệu cơ bản**
  - [x] Mẫu README ban đầu
  - [x] Mẫu CONTRIBUTING
  - **Kết quả:** Template sẵn sàng

---

### 🛠️ Phase 2: Phát triển Backend (2025-12-21 ~ 2025-12-24)

#### Thành viên 1 (Team Lead)
- ✅ **config.py**
  - [x] Cấu hình API Key
  - [x] Đường dẫn file
  - [x] Hằng số chung
  - **Thời gian:** 30 phút
  - **Kết quả:** 50 dòng code

- ✅ **data_loader.py** (Phần chính)
  - [x] Kết nối API OpenWeatherMap
  - [x] Parse JSON response
  - [x] Xử lý lỗi HTTP (401, 404, 429)
  - [x] Kiểm tra dữ liệu
  - [x] Lưu file CSV thô
  - **Thời gian:** 2 giờ
  - **Kết quả:** 170 dòng code + docstring

- ✅ **Kiểm tra & Debug**
  - [x] Test với API thực
  - [x] Fix lỗi phát hiện
  - [x] Kiểm tra edge cases
  - **Thời gian:** 1 giờ

#### Thành viên 2 (Dev Backend)
- ✅ **data_cleaner.py** (Phần chính)
  - [x] Đọc CSV thô
  - [x] Chuyển đổi thời gian DateTime
  - [x] Kiểm tra dữ liệu thiếu
  - [x] Kiểm tra dữ liệu trùng lặp
  - [x] Làm tròn số liệu
  - [x] Đổi tên cột sang Tiếng Việt
  - [x] Xử lý outlier
  - [x] Lưu file sạch
  - **Thời gian:** 2 giờ
  - **Kết quả:** 200 dòng code + docstring

- ✅ **statistics.py** (Module mới)
  - [x] Tính thống kê (mean, min, max, std, median)
  - [x] Phân tích xu hướng
  - [x] Tóm tắt thời tiết
  - [x] In báo cáo chi tiết
  - **Thời gian:** 1.5 giờ
  - **Kết quả:** 250 dòng code

- ✅ **Testing & Debug**
  - [x] Test hàm xử lý dữ liệu
  - [x] Kiểm tra thống kê
  - **Thời gian:** 1 giờ

---

### 🎨 Phase 3: Phát triển Frontend & Trực quan hóa (2025-12-24 ~ 2025-12-26)

#### Thành viên 3 (Dev Frontend)
- ✅ **visualizer.py** (Mở rộng)
  - [x] Biểu đồ kết hợp (Nhiệt độ + Độ ẩm)
  - [x] Histogram phân bố nhiệt độ
  - [x] Biểu đồ tốc gió (với mã màu)
  - [x] Thêm legend, grid, title
  - [x] Hàm create_all_charts()
  - **Thời gian:** 2 giờ
  - **Kết quả:** 300 dòng code

- ✅ **main.py** (Cải thiện)
  - [x] Thiết kế lại giao diện
  - [x] Thêm nút "Xem Thống Kê"
  - [x] Cải thiện thông báo lỗi
  - [x] Responsive layout
  - [x] Tối ưu resize ảnh
  - **Thời gian:** 1.5 giờ
  - **Kết quả:** 200 dòng code

- ✅ **Testing UI**
  - [x] Test các nút chức năng
  - [x] Test hiển thị biểu đồ
  - [x] Test thông báo lỗi
  - **Thời gian:** 1 giờ

#### Thành viên 1 & 2 (Hỗ trợ)
- ✅ **Tối ưu hóa code**
  - [x] Thêm type hints cho tất cả
  - [x] Viết docstring chi tiết (Google style)
  - [x] Kiểm tra PEP 8 compliance
  - **Thời gian:** 2 giờ

---

### 📚 Phase 4: Tài liệu & Báo cáo (2025-12-26 ~ 2025-12-27)

#### Thành viên 4 (QA / Tài liệu) - CHÍNH
- ✅ **README.md** (Chi tiết)
  - [x] Giới thiệu dự án
  - [x] Mô tả dữ liệu
  - [x] Hướng dẫn cài đặt (từng bước)
  - [x] Hướng dẫn sử dụng
  - [x] Kỹ thuật sử dụng
  - [x] Xử lý lỗi thường gặp
  - [x] Phát triển tiếp theo
  - **Thời gian:** 1.5 giờ
  - **Kết quả:** 500+ dòng

- ✅ **DATA_DICTIONARY.md**
  - [x] Mô tả chi tiết từng cột
  - [x] Phạm vi giá trị, kiểu dữ liệu
  - [x] Mối quan hệ giữa cột
  - [x] Hạn chế & khiếm khuyết
  - [x] Cách sử dụng dữ liệu
  - **Thời gian:** 1.5 giờ
  - **Kết quả:** 400+ dòng

- ✅ **CONTRIBUTING.md**
  - [x] Hướng dẫn báo cáo lỗi
  - [x] Hướng dẫn đề xuất tính năng
  - [x] Quy trình phát triển
  - [x] Style Guide
  - [x] Testing guide
  - [x] Commit message format
  - **Thời gian:** 1.5 giờ
  - **Kết quả:** 300+ dòng

- ✅ **CHANGELOG.md**
  - [x] Ghi lại v1.0.0
  - [x] Ghi lại v2.0.0 (all features)
  - [x] Kế hoạch v0.5.0
  - **Thời gian:** 1 giờ
  - **Kết quả:** 400+ dòng

- ✅ **WORK_DISTRIBUTION.md** (File này)
  - [x] Ghi chi tiết phân công
  - [x] Timeline thực tế
  - [x] Đóng góp từng người
  - **Thời gian:** 30 phút

#### Thành viên 1 (Team Lead)
- ✅ **Code Review**
  - [x] Review tất cả code
  - [x] Kiểm tra lỗi
  - [x] Yêu cầu cải thiện
  - **Thời gian:** 1 giờ

- ✅ **Testing toàn hệ thống**
  - [x] Test quy trình: API → Clean → Vẽ → GUI
  - [x] Test lỗi: API Key sai, thành phố sai, mạng lỗi
  - [x] Performance test
  - **Thời gian:** 1.5 giờ

#### Thành viên 5 (DevOps)
- ✅ **GitHub & Repository**
  - [x] Push tất cả code lên GitHub
  - [x] Tổ chức commit rõ ràng
  - [x] Tag phiên bản
  - **Thời gian:** 30 phút

- ✅ **Requirements & Environment**
  - [x] Cập nhật requirements.txt
  - [x] Hướng dẫn cài venv
  - [x] Test cài đặt từ scratch
  - **Thời gian:** 30 phút

---

## 📊 Tóm tắt Công việc

### Theo Thành viên

| Thành viên | Tác vụ chính | Thời gian | Đóng góp |
|-----------|------------|---------|---------|
| **TL (1)** | config.py, data_loader.py, Code Review, Testing | **6h** | 20% |
| **Dev 2** | data_cleaner.py, statistics.py, Testing | **5h** | 20% |
| **Dev 3** | visualizer.py, main.py, UI/UX Testing | **5h** | 20% |
| **QA (4)** | Tài liệu (README, DD, CONTRIBUTING, CHANGELOG) | **5.5h** | 20% |
| **DevOps (5)** | GitHub, Requirements, Environment | **1h** | 5% |
| **Chung** | Meetings, Coordination, Lên kế hoạch | **2h** | 10% |
| **TỔNG** | | **24.5h** | 100% |

### Theo Loại Công việc

| Loại | Số giờ | % |
|------|--------|---|
| **Code** (Backend/Frontend) | 11h | 45% |
| **Test & QA** | 3h | 12% |
| **Tài liệu** | 7h | 28% |
| **DevOps & Git** | 1h | 5% |
| **Quản lý & Họp** | 2.5h | 10% |

---

## 🎯 Mục tiêu đạt được

### ✅ Yêu cầu Bài Tập

| Yêu cầu | Thành viên | Trạng thái | Ghi chú |
|---------|-----------|-----------|--------|
| **2.1 Tìm hiểu dữ liệu** | TV2, TV4 | ✅ Hoàn thành | Mô tả rõ ràng ở README & DATA_DICTIONARY |
| **2.2 Xử lý dữ liệu** | TV1, TV2 | ✅ Hoàn thành | Làm sạch, chuẩn hóa, Numpy/Pandas |
| **Tổ chức modules** | TV1, TV2, TV3 | ✅ Hoàn thành | src/ package rõ ràng |
| **Làm sạch dữ liệu** | TV2 | ✅ Hoàn thành | Xóa lỗi, trùng, thiếu |
| **Chuẩn hóa dữ liệu** | TV2 | ✅ Hoàn thành | DateTime, tên Việt, làm tròn |
| **Vận dụng Numpy/Pandas** | TV2 | ✅ Hoàn thành | Sử dụng intensive |
| **Trực quan hóa Matplotlib** | TV3 | ✅ Hoàn thành | 3 biểu đồ |
| **Vẽ biểu đồ** | TV3 | ✅ Hoàn thành | Đa dạng loại biểu đồ |
| **Giao diện GUI** | TV3 | ✅ Hoàn thành | Tkinter, dễ dùng |
| **Báo cáo** | TV4 | ✅ Hoàn thành | 5 file tài liệu |
| **GitHub** | TV5 | ✅ Hoàn thành | Tracking đóng góp |
| **Phân công rõ** | Tất cả | ✅ Hoàn thành | File này |

### 📈 Thêm mở rộng vượt yêu cầu

- ✅ Module thống kê (statistics.py) - không yêu cầu
- ✅ Data Dictionary chi tiết - không yêu cầu
- ✅ Contributing guide - không yêu cầu
- ✅ Changelog - không yêu cầu
- ✅ Type hints & Google docstring - không yêu cầu
- ✅ Xử lý lỗi chi tiết - vượt yêu cầu
- ✅ Multiple charts - vượt yêu cầu

---

## 📅 Timeline Thực tế

```
Week 1:
  20/12 (T2) [10:00-12:00]  - Kick-off meeting (2h)
  20/12 (T2) [14:00-17:00]  - Phase 1: Design (3h)
  
  21/12 (T3) [08:00-12:00]  - TV1: config.py (3h)
  21/12 (T3) [14:00-16:30]  - TV2: data_loader prep (2.5h)
  
  22/12 (T4) [08:00-12:00]  - TV1: data_loader.py + test (4h)
  22/12 (T4) [09:00-12:00]  - TV2: data_cleaner.py (3h)
  22/12 (T4) [14:00-17:00]  - TV3: visualizer prep (3h)
  
  23/12 (T5) [08:00-12:00]  - TV2: statistics.py (3h)
  23/12 (T5) [09:00-12:00]  - TV1: Code review (3h)
  23/12 (T5) [14:00-17:00]  - TV3: visualizer implementation (3h)
  
  24/12 (CN) [Nghỉ - công đôi ngày khác]
  
  26/12 (T2) [08:00-12:00]  - TV3: main.py + UI (3h)
  26/12 (T2) [14:00-18:00]  - TV4: README + tài liệu (4h)
  
  27/12 (T3) [08:00-12:00]  - TV1: Testing (3h)
  27/12 (T3) [14:00-17:00]  - TV5: GitHub + Release (3h)
  27/12 (T3) [15:00-17:00]  - Tất cả: Final review (2h)

Tổng: ~55 giờ (bao gồm meeting & quản lý)
```

---

## 🏆 Đóng góp từng thành viên

### Thành viên 1 (Team Lead)
**Công việc:** 6 giờ chính + 1.5 giờ quản lý = **7.5h**
- ✅ Thiết kế kiến trúc (30 phút)
- ✅ config.py (30 phút)
- ✅ data_loader.py chi tiết (2h)
- ✅ Type hints & Docstring (1h)
- ✅ Code Review (1h)
- ✅ Testing toàn hệ thống (1.5h)
- ✅ Quản lý & Meeting (1.5h)

### Thành viên 2 (Dev Backend)
**Công việc:** 5 giờ chính + 1h quản lý = **6h**
- ✅ data_cleaner.py (2h)
- ✅ statistics.py (1.5h)
- ✅ Tối ưu code (1h)
- ✅ Testing (0.5h)
- ✅ Quản lý & Meeting (1h)

### Thành viên 3 (Dev Frontend)
**Công việc:** 5 giờ chính + 1h quản lý = **6h**
- ✅ visualizer.py (2h)
- ✅ main.py (1.5h)
- ✅ UI Testing (1h)
- ✅ Tối ưu front-end (0.5h)
- ✅ Quản lý & Meeting (1h)

### Thành viên 4 (QA / Tài liệu)
**Công việc:** 5.5 giờ chính + 0.5h quản lý = **6h**
- ✅ README.md (1.5h)
- ✅ DATA_DICTIONARY.md (1.5h)
- ✅ CONTRIBUTING.md (1.5h)
- ✅ CHANGELOG.md (1h)
- ✅ Git setup (30 phút)
- ✅ Quản lý & Meeting (0.5h)

### Thành viên 5 (DevOps)
**Công việc:** 1 giờ chính + 0.5h quản lý = **1.5h**
- ✅ GitHub setup (30 phút)
- ✅ Requirements.txt (20 phút)
- ✅ Environment testing (10 phút)
- ✅ Final release & tagging (30 phút)
- ✅ Meeting (0.5h)

---

## 🤝 Quy tắc làm việc nhóm

### Commit Policy
```
✅ Phải có meaningful commit message
✅ Commit ít nhất 3-5 lần/người/ngày
✅ Không commit code không test
❌ Không force push
❌ Không merge code review
```

### Code Review Process
1. Tạo Pull Request (từ feature branch)
2. Thành viên khác review (tối thiểu 1 người)
3. Approve trước khi merge
4. Delete branch sau merge

### Communication
- 📱 Chat hàng ngày qua Zalo/Discord
- 📊 Standup meeting 15 phút/sáng
- 🔔 Thông báo deadline 1 ngày trước
- 📋 Tracking tasks trên GitHub Projects

---

## 📝 Chữ ký & Xác nhận

| Thành viên | Ký | Ngày | Ghi chú |
|-----------|-----|------|--------|
| [Tên 1] | [ ] | | Đồng ý phân công |
| [Tên 2] | [ ] | | Đồng ý phân công |
| [Tên 3] | [ ] | | Đồng ý phân công |
| [Tên 4] | [ ] | | Đồng ý phân công |
| [Tên 5] | [ ] | | Đồng ý phân công |

---

**Tài liệu này sẽ được cập nhật nếu có thay đổi.**

*Phiên bản:* 1.0  
*Cập nhật lần cuối:* 2025-12-27
