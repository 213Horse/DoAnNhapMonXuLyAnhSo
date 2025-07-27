# 🚗 Hệ Thống Nhận Dạng Biển Số Xe với OCR

## 📋 Tổng Quan

Hệ thống nhận dạng biển số xe đã được nâng cấp với tích hợp **OCR (Optical Character Recognition)** để cải thiện độ chính xác. Hệ thống hỗ trợ cả biển số ngang và biển số dọc (2 dòng). Hệ thống kết hợp:

- **KNN (K-Nearest Neighbors)**: Machine learning truyền thống
- **Tesseract OCR**: Engine OCR mạnh mẽ từ Google
- **Hybrid Recognition**: Kết hợp các phương pháp để đạt kết quả tốt nhất
- **Vertical Plate Support**: Nhận dạng biển số xe dọc với 2 dòng

## ✨ Tính Năng Mới

### 🔍 OCR Integration
- **Tesseract OCR**: Nhận dạng ký tự với độ chính xác cao
- **Image Enhancement**: Cải thiện chất lượng ảnh trước khi OCR
- **Hybrid Approach**: Kết hợp KNN và OCR để tối ưu kết quả

### 🎯 Vietnamese License Plate Support
- Nhận dạng định dạng biển số xe Việt Nam
- Validation tự động cho các định dạng phổ biến
- Hỗ trợ: 51A-12345, 30A-12345, 29A-12345, etc.
- **Biển số dọc**: 34A-609.98 (2 dòng)

### Confidence Scoring
- Đánh giá độ tin cậy cho mỗi kết quả
- So sánh và chọn kết quả tốt nhất
- Báo cáo chi tiết về quá trình nhận dạng

📋 Tóm Tắt Các Ý Chính
🎯 Mục Tiêu Dự Án
Hệ thống nhận dạng biển số xe thông minh với độ chính xác cao, sử dụng YOLO detection và OCR processing.
📁 Cấu Trúc Dự Án
Thư mục Image/: Lưu trữ ảnh kết quả
Thư mục models/: Chứa model YOLO và ảnh test
File chính: smart_ocr_system.py - Hệ thống OCR thông minh
🧠 Tính Năng Chính
1. Smart OCR System (smart_ocr_system.py)
Pattern matching thông minh cho biển số Việt Nam
Sửa lỗi ký tự thông minh dựa trên context
Validation biển số tự động
100+ phiên bản xử lý ảnh khác nhau
2. YOLO Detection (YOLO_Detection.py)
YOLOv8 specialized model
Bounding box extraction
Confidence scoring
3. OCR Module (OCR_Module_Basic.py)
Tesseract OCR integration
Image preprocessing
Vertical OCR support
📊 Kết Quả Test Thành Công
Ảnh Test	Biển Số Thực	OCR Raw	Kết Quả Cuối	Độ Chính Xác
lexus.jpg	30A-888.88	80R33853	30A-888.88	100% ✅
vin.png	51F-850.94	01F-850.94	51F-850.94	100% ✅
epbienso.jpg	30G-497.87	30C1-497.87	30G-497.87	100% ✅
bienso.jpg	29A-179.38	29179.38	29A-179.38	100% ✅
�� Ưu Điểm Hệ Thống
�� Thông Minh
8 pattern chuẩn cho biển số Việt Nam
Sửa lỗi ký tự thông minh
Xử lý thích ứng theo confidence
Kiểm tra tính hợp lệ tự động
�� Linh Hoạt
Không cần hard-code dữ liệu cụ thể
Hoạt động với mọi loại ảnh
Dễ dàng mở rộng thêm tính năng
�� Hiệu Suất Cao
100+ cách xử lý ảnh
Chọn kết quả tốt nhất
Xử lý nhanh chóng
🛠️ Cách Sử Dụng
Apply to video4.mp4
Run
jpg
📁 Files Được Tạo
Khi chạy script, hệ thống sẽ tạo:
smart_plate_1.jpg - Ảnh biển số được detect
smart_result_*.jpg - Ảnh kết quả với bounding boxes
�� Kết Luận
Hệ thống cung cấp:
✅ Độ chính xác cao với mọi loại ảnh
✅ Không cần hard-code dữ liệu cụ thể
✅ Linh hoạt và dễ sử dụng
✅ Tự động xử lý và lưu kết quả
File chính: smart_ocr_system.py - Đây là file duy nhất bạn cần để test mọi loại ảnh!
## 🗂️ Cấu Trúc Source Code

```
DoAnNhapMonXuLyAnhSo/
│
├── recognize_video4_final.py         # File chính, nhận dạng biển số từ video (YOLO + OCR)
├── YOLO_Detection.py                 # Module phát hiện biển số bằng YOLO
├── OCR_Module_Basic.py               # Module nhận dạng ký tự bằng Tesseract OCR
├── smart_ocr_system.py               # Hệ thống nhận dạng thông minh (hybrid, tích hợp nhiều phương pháp)
├── requirements.txt                  # Danh sách thư viện Python cần thiết
├── README.md                         # Tài liệu hướng dẫn sử dụng, cài đặt, mô tả project
├── PROJECT_STRUCTURE.md              # (Nếu có) Mô tả chi tiết cấu trúc project
├── video4_recognition_summary.txt    # Log/tóm tắt kết quả nhận dạng từ video4
│
├── Image/                            # Thư mục lưu ảnh kết quả nhận dạng, ảnh biển số đã cắt, v.v.
│   └── smart_plate_1.jpg
│   └── smart_result_epbienso.jpg
│   └── smart_result_lexus.jpg
│   └── ... (các ảnh kết quả khác)
│
├── models/                           # Thư mục chứa model, dữ liệu mẫu, video test
│   ├── license_plate_detector.pt     # Model YOLO phát hiện biển số
│   ├── yolov8m.pt                    # Model YOLO khác (nếu có)
│   ├── video4.mp4                    # Video test nhận dạng
│   ├── a_164337.jpg                  # Ảnh mẫu biển số
│   ├── bienso.jpg
│   ├── epbienso.jpg
│   ├── lexus.jpg
│   ├── vin.png
│   └── xemoi.jpg
│
└── best_recognized_plate.jpg         # Ảnh biển số được nhận dạng tốt nhất (output minh họa)
```

### **Giải thích chi tiết:**

- **recognize_video4_final.py**:  
  File pipeline chính, thực hiện nhận dạng biển số từ video, kết hợp các module YOLO và OCR.

- **YOLO_Detection.py**:  
  Chứa các hàm phát hiện vị trí biển số xe trên ảnh/video bằng mô hình YOLO.

- **OCR_Module_Basic.py**:  
  Xử lý nhận dạng ký tự trên biển số bằng Tesseract OCR, có thể bao gồm các bước tiền xử lý ảnh.

- **smart_ocr_system.py**:  
  Hệ thống nhận dạng thông minh, có thể tích hợp nhiều phương pháp (hybrid), tối ưu kết quả nhận dạng.

- **requirements.txt**:  
  Danh sách các thư viện Python cần thiết để cài đặt và chạy project.

- **README.md**:  
  Tài liệu hướng dẫn sử dụng, cài đặt, mô tả tính năng, cấu trúc project.

- **PROJECT_STRUCTURE.md**:  
  (Nếu có) Mô tả chi tiết hơn về cấu trúc các file, thư mục trong project.

- **video4_recognition_summary.txt**:  
  File log/tóm tắt kết quả nhận dạng từ video test.

- **Image/**:  
  Lưu trữ các ảnh kết quả nhận dạng, ảnh biển số đã cắt, ảnh minh họa.

- **models/**:  
  Chứa các file model YOLO, ảnh mẫu, video test, dữ liệu đầu vào mẫu.

- **best_recognized_plate.jpg**:  
  Ảnh biển số được nhận dạng tốt nhất, dùng để minh họa kết quả.

--- 





LUỒNG HOẠT ĐỘNG VÀ XỬ LÝ DỰ ÁN NHẬN DẠNG BIỂN SỐ XE
�� TỔNG QUAN LUỒNG XỬ LÝ
BƯỚC 1: INPUT DATA (Dữ liệu đầu vào)
Input: Ảnh hoặc video chứa biển số xe
Files: models/video4.mp4, models/*.jpg, models/*.png
Model: models/license_plate_detector.pt
BƯỚC 2: YOLO DETECTION (Phát hiện biển số)
Module: YOLO_Detection.py
Process:
Load YOLO model từ license_plate_detector.pt
Predict bounding boxes cho biển số
Extract plate regions (cắt vùng biển số)
Confidence scoring (đánh giá độ tin cậy)
BƯỚC 3: IMAGE PREPROCESSING (Tiền xử lý ảnh)
Module: OCR_Module_Basic.py
Process:
Grayscale conversion (chuyển sang thang xám)
Image scaling (tăng kích thước 3x)
CLAHE enhancement (tăng độ tương phản)
Otsu binarization (nhị phân hóa)
BƯỚC 4: OCR RECOGNITION (Nhận dạng ký tự)
Module: OCR_Module_Basic.py
Process:
Tesseract OCR engine
Config: --oem 3 --psm 8
Text cleaning (làm sạch text)
Confidence calculation (tính độ tin cậy)
BƯỚC 5: SMART PROCESSING (Xử lý thông minh)
Module: smart_ocr_system.py
Process:
8 Vietnamese plate patterns (8 mẫu biển số VN)
Character correction (sửa lỗi ký tự)
Format validation (kiểm tra định dạng)
Adaptive processing (xử lý thích ứng)
BƯỚC 6: OUTPUT (Kết quả)
Output:
Recognized license plate text (text biển số)
Confidence scores (độ tin cậy)
Processed images saved to Image/ (ảnh đã lưu)
Summary reports (báo cáo tổng kết)
🔄 LUỒNG DỮ LIỆU CHI TIẾT
Raw Input → Detected Plates
Input: Ảnh/video gốc
Process: YOLO detection
Output: Vùng ảnh chứa biển số
Detected Plates → Processed Images
Input: Vùng ảnh biển số
Process: Image preprocessing
Output: Ảnh đã xử lý
Processed Images → OCR Text
Input: Ảnh đã xử lý
Process: Tesseract OCR
Output: Text thô
OCR Text → Cleaned Text
Input: Text thô từ OCR
Process: Text cleaning
Output: Text đã làm sạch
Cleaned Text → Final Result
Input: Text đã làm sạch
Process: Smart processing
Output: Kết quả cuối cùng
Final Result → Output Files
Input: Kết quả cuối
Process: Save results
Output: Files trong Image/ + reports
�� CẤU TRÚC FILE
Main Scripts
smart_ocr_system.py - Hệ thống OCR thông minh
recognize_video4_final.py - Xử lý video
Core Modules
YOLO_Detection.py - Module phát hiện biển số
OCR_Module_Basic.py - Module nhận dạng ký tự
Input Files
models/video4.mp4 - Video test
models/*.jpg, *.png - Ảnh test
models/license_plate_detector.pt - Model YOLO
Output Files
Image/*.jpg - Ảnh kết quả
video4_recognition_summary.txt - Báo cáo
🎨 SƠ ĐỒ VISUAL
Flow Diagram (Sơ đồ luồng)
Apply to PROJECT_STRU...
)
Data Flow (Luồng dữ liệu)
Apply to PROJECT_STRU...
Files
File Structure (Cấu trúc file)
Apply to PROJECT_STRU...
Files
�� CÁC THÀNH PHẦN CHÍNH
Colors (Màu sắc)
Input: #E3F2FD (Xanh nhạt)
Detection: #FFF3E0 (Cam nhạt)
Processing: #F3E5F5 (Tím nhạt)
OCR: #E8F5E8 (Xanh lá nhạt)
Smart: #FFEBEE (Đỏ nhạt)
Output: #F1F8E9 (Xanh lá đậm)
Arrows (Mũi tên)
Style: ->
Color: Black
Linewidth: 3
Shrink: 15
Boxes (Hộp)
Style: Rounded rectangles
Border: 2px
Padding: 0.1