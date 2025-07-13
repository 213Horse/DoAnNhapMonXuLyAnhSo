# Sơ Đồ Dự Án: Hệ Thống Nhận Dạng Biển Số Xe

## 1. Tổng Quan Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    HỆ THỐNG NHẬN DẠNG BIỂN SỐ XE              │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Kiến Trúc Tổng Thể

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Image   │───▶│  Preprocessing  │───▶│ Plate Detection │
│   (vin.jpg)     │    │   (Preprocess)  │    │ (DetectPlates)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Output Text   │◀───│  Char Detection │◀───│  Plate Images   │
│  (License No.)  │    │  (DetectChars)  │    │ (PossiblePlate) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 3. Luồng Xử Lý Chi Tiết

### 3.1. Giai Đoạn 1: Tiền Xử Lý (Preprocessing)
```
Input Image
     │
     ▼
┌─────────────────┐
│ Extract Value   │ ◀── Chuyển đổi sang HSV và lấy kênh Value
│ (extractValue)  │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│Maximize Contrast│ ◀── TopHat + BlackHat morphology
│(maximizeContrast)│
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Gaussian Blur   │ ◀── Làm mịn ảnh
└─────────────────┘
     │
     ▼
┌─────────────────┐
│Adaptive Threshold│ ◀── Nhị phân hóa thích ứng
└─────────────────┘
```

### 3.2. Giai Đoạn 2: Phát Hiện Biển Số (Plate Detection)
```
Preprocessed Image
        │
        ▼
┌─────────────────┐
│Find Contours    │ ◀── Tìm tất cả contour
│(findContours)   │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│Filter Possible  │ ◀── Lọc contour có thể là ký tự
│Chars            │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│Group Matching   │ ◀── Nhóm các ký tự tương tự
│Chars            │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│Extract Plate    │ ◀── Trích xuất vùng biển số
│Regions          │
└─────────────────┘
```

### 3.3. Giai Đoạn 3: Nhận Dạng Ký Tự (Character Recognition)
```
Plate Image
    │
    ▼
┌─────────────────┐
│Preprocess Plate │ ◀── Tiền xử lý ảnh biển số
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Find Characters  │ ◀── Tìm các ký tự trong biển số
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Group Characters │ ◀── Nhóm ký tự thành chuỗi
└─────────────────┘
    │
    ▼
┌─────────────────┐
│KNN Recognition  │ ◀── Nhận dạng bằng KNN
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Output Text      │ ◀── Kết quả nhận dạng
└─────────────────┘
```

## 4. Cấu Trúc Module

### 4.1. Main.py - Điều Khiển Chính
```
┌─────────────────────────────────────────────────────────────┐
│                        Main.py                             │
├─────────────────────────────────────────────────────────────┤
│ • main() - Hàm chính điều khiển toàn bộ quá trình        │
│ • drawRedRectangleAroundPlate() - Vẽ khung đỏ quanh biển  │
│ • writeLicensePlateCharsOnImage() - Ghi text lên ảnh      │
│ • Các hằng số màu sắc (SCALAR_BLACK, SCALAR_WHITE, ...)  │
└─────────────────────────────────────────────────────────────┘
```

### 4.2. Preprocess.py - Tiền Xử Lý
```
┌─────────────────────────────────────────────────────────────┐
│                     Preprocess.py                          │
├─────────────────────────────────────────────────────────────┤
│ • preprocess() - Hàm chính tiền xử lý                     │
│ • extractValue() - Trích xuất kênh Value từ HSV           │
│ • maximizeContrast() - Tăng độ tương phản                 │
│ • Các hằng số filter và threshold                         │
└─────────────────────────────────────────────────────────────┘
```

### 4.3. DetectPlates.py - Phát Hiện Biển Số
```
┌─────────────────────────────────────────────────────────────┐
│                    DetectPlates.py                         │
├─────────────────────────────────────────────────────────────┤
│ • detectPlatesInScene() - Phát hiện biển số trong ảnh     │
│ • findPossibleCharsInScene() - Tìm ký tự có thể trong ảnh │
│ • extractPlate() - Trích xuất vùng biển số                │
│ • Các hằng số padding cho biển số                         │
└─────────────────────────────────────────────────────────────┘
```

### 4.4. DetectChars.py - Nhận Dạng Ký Tự
```
┌─────────────────────────────────────────────────────────────┐
│                    DetectChars.py                          │
├─────────────────────────────────────────────────────────────┤
│ • loadKNNDataAndTrainKNN() - Huấn luyện KNN               │
│ • detectCharsInPlates() - Nhận dạng ký tự trong biển số   │
│ • findPossibleCharsInPlate() - Tìm ký tự trong biển số    │
│ • findListOfListsOfMatchingChars() - Nhóm ký tự tương tự  │
│ • recognizeCharsInPlate() - Nhận dạng ký tự bằng KNN      │
│ • Các hàm hỗ trợ: distanceBetweenChars(), angleBetweenChars() │
└─────────────────────────────────────────────────────────────┘
```

### 4.5. PossiblePlate.py - Cấu Trúc Dữ Liệu Biển Số
```
┌─────────────────────────────────────────────────────────────┐
│                   PossiblePlate.py                         │
├─────────────────────────────────────────────────────────────┤
│ class PossiblePlate:                                       │
│   • imgPlate - Ảnh biển số                                │
│   • imgGrayscale - Ảnh grayscale                          │
│   • imgThresh - Ảnh threshold                             │
│   • rrLocationOfPlateInScene - Vị trí biển số trong ảnh   │
│   • strChars - Chuỗi ký tự nhận dạng được                 │
└─────────────────────────────────────────────────────────────┘
```

### 4.6. PossibleChar.py - Cấu Trúc Dữ Liệu Ký Tự
```
┌─────────────────────────────────────────────────────────────┐
│                   PossibleChar.py                          │
├─────────────────────────────────────────────────────────────┤
│ class PossibleChar:                                        │
│   • contour - Contour của ký tự                           │
│   • boundingRect - Hình chữ nhật bao quanh               │
│   • intCenterX, intCenterY - Tọa độ tâm                   │
│   • intBoundingRectWidth, intBoundingRectHeight - Kích thước │
│   • fltAspectRatio - Tỷ lệ khung hình                     │
│   • fltDiagonalSize - Đường chéo                           │
└─────────────────────────────────────────────────────────────┘
```

## 5. Dữ Liệu Huấn Luyện

```
┌─────────────────────────────────────────────────────────────┐
│                    Training Data                           │
├─────────────────────────────────────────────────────────────┤
│ • classifications.txt - Nhãn các ký tự (0-9, A-Z)        │
│ • flattened_images.txt - Ảnh ký tự đã làm phẳng           │
│ • KNN Model - Mô hình K-Nearest Neighbors đã huấn luyện   │
└─────────────────────────────────────────────────────────────┘
```

## 6. Thư Mục Dữ Liệu

```
┌─────────────────────────────────────────────────────────────┐
│                   LicPlateImages/                          │
├─────────────────────────────────────────────────────────────┤
│ • vin.jpg - Ảnh mẫu chính                                 │
│ • vn1.jpg, vn2.png, ... - Các ảnh biển số Việt Nam       │
│ • 1.png, 2.png, ... - Ảnh biển số khác                   │
└─────────────────────────────────────────────────────────────┘
```

## 7. Các Hằng Số Quan Trọng

### 7.1. Hằng Số Phát Hiện Ký Tự
```
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0
MIN_PIXEL_AREA = 80
```

### 7.2. Hằng Số So Sánh Ký Tự
```
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0
MAX_CHANGE_IN_AREA = 0.5
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 12.0
```

### 7.3. Hằng Số Nhận Dạng
```
MIN_NUMBER_OF_MATCHING_CHARS = 3
RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30
MIN_CONTOUR_AREA = 100
```

## 8. Luồng Xử Lý Hoàn Chỉnh

```
1. Load Image (vin.jpg)
   │
   ▼
2. Preprocess Image
   ├── Convert to HSV
   ├── Extract Value channel
   ├── Maximize contrast
   ├── Gaussian blur
   └── Adaptive threshold
   │
   ▼
3. Find All Contours
   │
   ▼
4. Filter Possible Characters
   ├── Check pixel area
   ├── Check aspect ratio
   └── Check dimensions
   │
   ▼
5. Group Matching Characters
   ├── Distance between chars
   ├── Angle between chars
   ├── Size similarity
   └── Area similarity
   │
   ▼
6. Extract Plate Regions
   ├── Calculate plate center
   ├── Calculate plate dimensions
   ├── Calculate rotation angle
   └── Extract rotated region
   │
   ▼
7. Preprocess Plate Images
   ├── Resize for better detection
   └── Re-threshold
   │
   ▼
8. Find Characters in Plates
   │
   ▼
9. Group Characters in Plates
   │
   ▼
10. Remove Overlapping Characters
    │
    ▼
11. KNN Character Recognition
    ├── Resize to 20x30
    ├── Flatten to 1D array
    └── KNN classification
    │
    ▼
12. Output License Plate Text
```

## 9. Kết Quả Đầu Ra

```
┌─────────────────────────────────────────────────────────────┐
│                    Output Results                          │
├─────────────────────────────────────────────────────────────┤
│ • imgOriginalScene.png - Ảnh gốc với kết quả vẽ lên       │
│ • Console output - Text biển số nhận dạng được            │
│ • Debug windows - Các cửa sổ hiển thị từng bước (nếu bật) │
└─────────────────────────────────────────────────────────────┘
```

## 10. Công Nghệ Sử Dụng

```
┌─────────────────────────────────────────────────────────────┐
│                    Technologies                            │
├─────────────────────────────────────────────────────────────┤
│ • OpenCV - Xử lý ảnh và computer vision                   │
│ • NumPy - Tính toán số học                                │
│ • K-Nearest Neighbors (KNN) - Machine learning            │
│ • Python - Ngôn ngữ lập trình chính                       │
│ • Morphological Operations - Xử lý hình thái học          │
│ • Contour Detection - Phát hiện đường viền                │
└─────────────────────────────────────────────────────────────┘
``` 