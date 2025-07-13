# Tóm Tắt Dự Án: Hệ Thống Nhận Dạng Biển Số Xe

## 📋 Thông Tin Dự Án

**Tên dự án:** Hệ Thống Nhận Dạng Biển Số Xe  
**Ngôn ngữ:** Python  
**Thư viện chính:** OpenCV, NumPy  
**Thuật toán ML:** K-Nearest Neighbors (KNN)  
**Mục đích:** Nhận dạng và trích xuất text từ biển số xe trong ảnh

## 🎯 Mục Tiêu

- Phát hiện vùng biển số xe trong ảnh
- Trích xuất và nhận dạng các ký tự trên biển số
- Xuất kết quả dưới dạng text

## 🏗️ Kiến Trúc Hệ Thống

### Các Module Chính:

1. **Main.py** - Điều khiển chính, khởi tạo và điều phối toàn bộ quá trình
2. **Preprocess.py** - Tiền xử lý ảnh (chuyển HSV, tăng độ tương phản, nhị phân hóa)
3. **DetectPlates.py** - Phát hiện biển số xe trong ảnh
4. **DetectChars.py** - Nhận dạng ký tự bằng thuật toán KNN
5. **PossiblePlate.py** - Cấu trúc dữ liệu cho biển số
6. **PossibleChar.py** - Cấu trúc dữ liệu cho ký tự

## 🔄 Quy Trình Xử Lý

### Bước 1: Tiền Xử Lý
- Chuyển đổi ảnh sang không gian màu HSV
- Trích xuất kênh Value
- Tăng độ tương phản bằng morphological operations
- Làm mịn ảnh bằng Gaussian blur
- Nhị phân hóa thích ứng

### Bước 2: Phát Hiện Biển Số
- Tìm tất cả contour trong ảnh
- Lọc contour có thể là ký tự (dựa trên kích thước, tỷ lệ)
- Nhóm các ký tự tương tự thành chuỗi
- Trích xuất vùng biển số từ các nhóm ký tự

### Bước 3: Nhận Dạng Ký Tự
- Tiền xử lý ảnh biển số
- Tìm các ký tự trong biển số
- Loại bỏ ký tự chồng lấp
- Nhận dạng từng ký tự bằng KNN
- Ghép thành chuỗi kết quả

## 📊 Dữ Liệu Huấn Luyện

- **classifications.txt**: Nhãn các ký tự (0-9, A-Z)
- **flattened_images.txt**: Ảnh ký tự đã làm phẳng
- **KNN Model**: Mô hình đã được huấn luyện

## 🎛️ Các Tham Số Quan Trọng

### Phát Hiện Ký Tự:
- `MIN_PIXEL_WIDTH = 2`
- `MIN_PIXEL_HEIGHT = 8`
- `MIN_ASPECT_RATIO = 0.25`
- `MAX_ASPECT_RATIO = 1.0`
- `MIN_PIXEL_AREA = 80`

### So Sánh Ký Tự:
- `MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3`
- `MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0`
- `MAX_CHANGE_IN_AREA = 0.5`
- `MAX_ANGLE_BETWEEN_CHARS = 12.0`

### Nhận Dạng:
- `RESIZED_CHAR_IMAGE_WIDTH = 20`
- `RESIZED_CHAR_IMAGE_HEIGHT = 30`
- `MIN_NUMBER_OF_MATCHING_CHARS = 3`

## 📁 Cấu Trúc Thư Mục

```
DoAnNhapMonXuLyAnhSo/
├── Main.py                    # Điều khiển chính
├── Preprocess.py              # Tiền xử lý ảnh
├── DetectPlates.py            # Phát hiện biển số
├── DetectChars.py             # Nhận dạng ký tự
├── PossiblePlate.py           # Class biển số
├── PossibleChar.py            # Class ký tự
├── classifications.txt        # Dữ liệu huấn luyện
├── flattened_images.txt       # Dữ liệu huấn luyện
├── LicPlateImages/            # Ảnh mẫu
│   ├── vin.jpg               # Ảnh chính
│   ├── vn1.jpg, vn2.png...  # Ảnh biển số VN
│   └── 1.png, 2.png...      # Ảnh khác
└── README.md
```

## 🚀 Cách Sử Dụng

1. **Chuẩn bị môi trường:**
   ```bash
   pip install opencv-python numpy
   ```

2. **Chạy chương trình:**
   ```bash
   python Main.py
   ```

3. **Kết quả:**
   - Text biển số được in ra console
   - Ảnh kết quả được lưu thành `imgOriginalScene.png`
   - Các cửa sổ debug hiển thị từng bước (nếu `showSteps = True`)

## 🔧 Tính Năng

### ✅ Đã Hoàn Thành:
- Phát hiện biển số xe trong ảnh
- Nhận dạng ký tự bằng KNN
- Xử lý ảnh với OpenCV
- Hiển thị kết quả trực quan
- Debug mode với các bước chi tiết

### 🔄 Có Thể Cải Tiến:
- Tăng độ chính xác nhận dạng
- Hỗ trợ nhiều loại biển số khác nhau
- Tối ưu hóa tốc độ xử lý
- Giao diện người dùng
- Xử lý ảnh thời gian thực

## 📈 Hiệu Suất

- **Độ chính xác:** Phụ thuộc vào chất lượng ảnh đầu vào
- **Tốc độ:** Xử lý ảnh trong vài giây
- **Hỗ trợ:** Biển số xe Việt Nam và quốc tế

## 🛠️ Công Nghệ Sử Dụng

- **OpenCV:** Xử lý ảnh và computer vision
- **NumPy:** Tính toán số học
- **KNN:** Machine learning cho nhận dạng ký tự
- **Morphological Operations:** Xử lý hình thái học
- **Contour Detection:** Phát hiện đường viền

## 📝 Ghi Chú

- Dự án sử dụng thuật toán KNN đơn giản cho nhận dạng ký tự
- Có thể cải thiện bằng các thuật toán deep learning hiện đại
- Cần dữ liệu huấn luyện đa dạng hơn để tăng độ chính xác
- Hệ thống hoạt động tốt với ảnh có chất lượng tốt và biển số rõ ràng

## 🔗 Liên Kết

- **Sơ đồ dự án:** `project_diagram.md`
- **Sơ đồ UML:** `UML_diagram.md`
- **Mã nguồn:** Các file `.py` trong thư mục gốc 