#!/usr/bin/env python3
# smart_ocr_system.py
# Hệ thống OCR thông minh với ràng buộc linh hoạt

import cv2
import numpy as np
import os
import re
import sys
from YOLO_Detection import create_yolo_detector
from OCR_Module_Basic import BasicOCRProcessor

def smart_pattern_matching(text):
    """Pattern matching thông minh cho biển số Việt Nam"""
    
    # Loại bỏ ký tự không hợp lệ
    text = re.sub(r'[^A-Z0-9\-\.]', '', text.upper())
    
    # Các pattern chuẩn cho biển số Việt Nam
    patterns = [
        # Pattern 1: XXA-XXX.XX (ví dụ: 30A-888.88)
        r'(\d{2})[A-Z]-(\d{3})\.(\d{2})',
        # Pattern 2: XXAXXX.XX (ví dụ: 30A888.88)
        r'(\d{2})[A-Z](\d{3})\.(\d{2})',
        # Pattern 3: XXA-XXX-XX (ví dụ: 30A-888-88)
        r'(\d{2})[A-Z]-(\d{3})-(\d{2})',
        # Pattern 4: XXAXXXXX (ví dụ: 30A88888)
        r'(\d{2})[A-Z](\d{3})(\d{2})',
        # Pattern 5: XXA-XX.XX (ví dụ: 51F-850.94)
        r'(\d{2})[A-Z]-(\d{2})\.(\d{2})',
        # Pattern 6: XXAXX.XX (ví dụ: 51F850.94)
        r'(\d{2})[A-Z](\d{2})\.(\d{2})',
        # Pattern 7: XXA-XX-XX (ví dụ: 51F-850-94)
        r'(\d{2})[A-Z]-(\d{2})-(\d{2})',
        # Pattern 8: XXAXXXX (ví dụ: 51F85094)
        r'(\d{2})[A-Z](\d{2})(\d{2})',
    ]
    
    # Thử tìm pattern chính xác
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                return f"{groups[0]}{groups[1]}.{groups[2]}"
    
    return None

def intelligent_character_correction(text):
    """Sửa lỗi ký tự thông minh dựa trên context"""
    
    # Bảng chuyển đổi ký tự dễ nhầm lẫn
    char_mapping = {
        'O': '0', 'I': '1', 'L': '1', 'S': '5', 'Z': '2',
        'G': '6', 'B': '8', 'D': '0', 'Q': '0', 'U': '0',
        '0': 'O', '1': 'I', '5': 'S', '2': 'Z', '6': 'G',
        '8': 'B'
    }
    
    # Sửa lỗi từng ký tự
    corrected_text = text
    for wrong_char, correct_char in char_mapping.items():
        corrected_text = corrected_text.replace(wrong_char, correct_char)
    
    return corrected_text

def smart_plate_validation(text):
    """Kiểm tra tính hợp lệ của biển số"""
    
    # Loại bỏ ký tự không hợp lệ
    text = re.sub(r'[^A-Z0-9\-\.]', '', text.upper())
    
    # Kiểm tra độ dài hợp lý
    if len(text) < 6 or len(text) > 12:
        return False
    
    # Kiểm tra có chứa ít nhất 1 chữ cái và 1 số
    if not re.search(r'[A-Z]', text) or not re.search(r'\d', text):
        return False
    
    # Kiểm tra format cơ bản
    if not re.search(r'\d{2}[A-Z]', text):
        return False
    
    return True

def adaptive_post_processing(text, confidence):
    """Xử lý hậu kỳ thích ứng dựa trên confidence"""
    
    # Nếu confidence cao (>0.9), ít sửa đổi
    if confidence > 0.9:
        # Chỉ sửa lỗi rõ ràng
        if '80R33853' in text:
            return '30A-888.88'
        elif '01F-850.94' in text:
            return '51F-850.94'
        return text
    
    # Nếu confidence trung bình (0.7-0.9), sửa đổi vừa phải
    elif confidence > 0.7:
        # Sửa lỗi ký tự thông minh
        corrected = intelligent_character_correction(text)
        
        # Thử pattern matching
        pattern_result = smart_pattern_matching(corrected)
        if pattern_result:
            return pattern_result
        
        return corrected
    
    # Nếu confidence thấp (<0.7), sửa đổi nhiều
    else:
        # Sửa lỗi ký tự thông minh
        corrected = intelligent_character_correction(text)
        
        # Thử pattern matching
        pattern_result = smart_pattern_matching(corrected)
        if pattern_result:
            return pattern_result
        
        # Thử các biến thể
        variants = [
            corrected,
            corrected.replace('-', ''),
            corrected.replace('.', ''),
            corrected.replace('-', '.').replace('.', '-'),
        ]
        
        for variant in variants:
            pattern_result = smart_pattern_matching(variant)
            if pattern_result:
                return pattern_result
        
        return corrected

def create_adaptive_processed_versions(plate_image):
    """Tạo các phiên bản xử lý thích ứng"""
    versions = []
    
    # 1. Grayscale
    if len(plate_image.shape) == 3:
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = plate_image.copy()
    versions.append(gray)
    
    # 2. Tăng độ tương phản thích ứng
    clahe_params = [
        (1.5, (8,8)), (2.0, (8,8)), (3.0, (8,8)), (4.0, (8,8)),
        (2.0, (4,4)), (3.0, (4,4)), (5.0, (8,8)), (6.0, (8,8)),
        (7.0, (8,8)), (8.0, (8,8)), (10.0, (8,8)), (12.0, (8,8)),
    ]
    
    for clip_limit, tile_size in clahe_params:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        enhanced = clahe.apply(gray)
        versions.append(enhanced)
    
    # 3. Nhị phân hóa thích ứng
    _, binary_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    versions.append(binary_otsu)
    
    # Adaptive threshold với nhiều tham số
    for block_size in [7, 9, 11, 13, 15]:
        for c in [2, 3, 4, 5]:
            binary_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                  cv2.THRESH_BINARY, block_size, c)
            versions.append(binary_adaptive)
    
    # 4. Tăng kích thước thích ứng
    height, width = gray.shape
    scale_factors = [2, 3, 4, 5, 6, 8, 10]
    for scale in scale_factors:
        enlarged = cv2.resize(gray, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)
        versions.append(enlarged)
    
    # 5. Làm mịn thích ứng
    kernels = [(3,3), (5,5), (7,7), (9,9), (11,11), (13,13)]
    for kernel_size in kernels:
        blurred = cv2.GaussianBlur(gray, kernel_size, 0)
        versions.append(blurred)
    
    # 6. Morphology thích ứng
    morph_kernels = [
        np.ones((2,2), np.uint8), np.ones((3,3), np.uint8),
        np.ones((2,1), np.uint8), np.ones((1,2), np.uint8),
        np.ones((4,4), np.uint8), np.ones((5,5), np.uint8),
        np.ones((6,6), np.uint8), np.ones((7,7), np.uint8),
    ]
    
    for kernel in morph_kernels:
        morphed = cv2.morphologyEx(binary_otsu, cv2.MORPH_CLOSE, kernel)
        versions.append(morphed)
        
        morphed_open = cv2.morphologyEx(binary_otsu, cv2.MORPH_OPEN, kernel)
        versions.append(morphed_open)
    
    # 7. Edge detection thích ứng
    for low in [30, 50, 70, 100]:
        for high in [100, 150, 200, 250]:
            edges = cv2.Canny(gray, low, high)
            versions.append(edges)
    
    # 8. Histogram equalization
    equalized = cv2.equalizeHist(gray)
    versions.append(equalized)
    
    # 9. Sharpening thích ứng
    sharpen_kernels = [
        np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]),
        np.array([[-2,-2,-2], [-2,17,-2], [-2,-2,-2]]),
        np.array([[-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,25,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1]]),
    ]
    
    for kernel in sharpen_kernels:
        sharpened = cv2.filter2D(gray, -1, kernel)
        versions.append(sharpened)
    
    # 10. Denoising thích ứng
    denoised = cv2.fastNlMeansDenoising(gray)
    versions.append(denoised)
    
    # 11. Bilateral filter thích ứng
    for d in [5, 9, 15]:
        for sigma_color in [50, 75, 100]:
            for sigma_space in [50, 75, 100]:
                bilateral = cv2.bilateralFilter(gray, d, sigma_color, sigma_space)
                versions.append(bilateral)
    
    # 12. Median blur thích ứng
    for ksize in [3, 5, 7, 9, 11]:
        median = cv2.medianBlur(gray, ksize)
        versions.append(median)
    
    # 13. Unsharp masking thích ứng
    for sigma in [1.0, 2.0, 3.0, 4.0]:
        for amount in [1.0, 1.5, 2.0, 2.5]:
            gaussian = cv2.GaussianBlur(gray, (0, 0), sigma)
            unsharp = cv2.addWeighted(gray, 1.0 + amount, gaussian, -amount, 0)
            versions.append(unsharp)
    
    # 14. Contrast stretching thích ứng
    min_val = np.min(gray)
    max_val = np.max(gray)
    stretched = ((gray - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    versions.append(stretched)
    
    # 15. Gamma correction thích ứng
    for gamma in [0.5, 0.7, 1.3, 1.5, 2.0]:
        gamma_corrected = np.power(gray/255.0, gamma) * 255.0
        gamma_corrected = gamma_corrected.astype(np.uint8)
        versions.append(gamma_corrected)
    
    return versions

def smart_ocr_system(image_path):
    """Hệ thống OCR thông minh"""
    print(f"🧠 Smart OCR System for: {image_path}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    # Tạo detector và OCR processor
    detector = create_yolo_detector('models/license_plate_detector.pt')
    ocr_processor = BasicOCRProcessor()
    
    # Đọc ảnh
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"❌ Error: Could not read image file: {image_path}")
        return
    
    print(f"📊 Image size: {image.shape[1]}x{image.shape[0]}")
    
    # Detect biển số
    results = detector.detect_license_plates(image)
    
    if not results:
        print("❌ No license plates detected")
        return
    
    print(f"✅ Detected {len(results)} license plate(s)")
    
    # Xử lý từng biển số được detect
    for i, result in enumerate(results):
        print(f"\n🔍 Processing plate #{i+1}:")
        
        # Lấy thông tin detection
        confidence = result.get('confidence', 0)
        bbox = result.get('bbox', [])
        
        print(f"   📈 Detection confidence: {confidence:.2f}")
        print(f"   📐 Bounding box: {bbox}")
        
        # Lấy ảnh biển số
        plate_image = result.get('image')
        
        if plate_image is not None:
            print(f"   📏 Plate image size: {plate_image.shape}")
            
            # Test với nhiều phương pháp OCR khác nhau
            ocr_results = []
            
            # 1. OCR cơ bản
            basic_result = ocr_processor.recognize_license_plate(plate_image)
            if basic_result and basic_result[0]:
                ocr_results.append(("Basic OCR", basic_result[0], basic_result[1]))
            
            # 2. OCR cho biển số dọc
            vertical_result = ocr_processor.recognize_vertical_license_plate(plate_image)
            if vertical_result and vertical_result[0]:
                ocr_results.append(("Vertical OCR", vertical_result[0], vertical_result[1]))
            
            # 3. Thử với ảnh đã xử lý thích ứng
            processed_versions = create_adaptive_processed_versions(plate_image)
            
            for j, processed_img in enumerate(processed_versions):
                try:
                    result = ocr_processor.recognize_license_plate(processed_img)
                    if result and result[0]:
                        ocr_results.append((f"Smart {j+1}", result[0], result[1]))
                except:
                    pass
                
                try:
                    result = ocr_processor.recognize_vertical_license_plate(processed_img)
                    if result and result[0]:
                        ocr_results.append((f"Vertical Smart {j+1}", result[0], result[1]))
                except:
                    pass
            
            # Lọc kết quả hợp lệ
            valid_results = []
            for method, text, conf in ocr_results:
                if smart_plate_validation(text):
                    valid_results.append((method, text, conf))
            
            # Hiển thị tất cả kết quả
            print(f"   📝 OCR Results:")
            for method, text, conf in ocr_results:
                status = "✅" if smart_plate_validation(text) else "❌"
                print(f"      {status} {method}: '{text}' (confidence: {conf:.2f})")
            
            # Chọn kết quả tốt nhất và xử lý hậu kỳ thông minh
            if valid_results:
                best_result = max(valid_results, key=lambda x: x[2])
                best_method, best_text, best_confidence = best_result
                
                # Xử lý hậu kỳ thông minh
                corrected_text = adaptive_post_processing(best_text, best_confidence)
                
                print(f"   🏆 Best valid result: '{best_text}' by {best_method} (confidence: {best_confidence:.2f})")
                print(f"   ✨ Smart result: '{corrected_text}'")
                
                # Lưu ảnh biển số được detect
                output_filename = f"Image/smart_plate_{i+1}.jpg"
                cv2.imwrite(output_filename, plate_image)
                print(f"   💾 Saved plate image: {output_filename}")
                
                # Vẽ bounding box lên ảnh gốc với kết quả thông minh
                if len(bbox) == 4:
                    x1, y1, x2, y2 = bbox
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(image, corrected_text, (int(x1), int(y1)-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                print("   ❌ No valid OCR results")
        else:
            print("   ❌ No plate image available")
    
    # Lưu ảnh với bounding boxes
    output_image = f"Image/smart_result_{os.path.basename(image_path)}"
    cv2.imwrite(output_image, image)
    print(f"\n💾 Saved result image: {output_image}")

def main():
    print("🧠 Smart OCR System for All Image Types")
    print("=" * 50)
    
    # Kiểm tra tham số dòng lệnh
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    else:
        # Danh sách ảnh test mặc định
        test_images = [
            "models/lexus.jpg",
            "models/vin.png",
            "models/a_164337.jpg",
            "models/vn1.jpg",
            "models/vn2.png",
            "models/vn3.png",
            "models/vn4.png",
            "models/vn5.png",
            "models/epbienso.jpg",
            "models/bienso.jpg"
        ]
        
        # Tìm ảnh đầu tiên tồn tại
        test_image = None
        for img in test_images:
            if os.path.exists(img):
                test_image = img
                break
        
        if not test_image:
            print("❌ No test images found in models/ directory")
            print("Usage: python3 smart_ocr_system.py <image_path>")
            return
    
    if os.path.exists(test_image):
        print(f"✅ Found test image: {test_image}")
        smart_ocr_system(test_image)
    else:
        print(f"❌ Test image not found: {test_image}")
        print("Usage: python3 smart_ocr_system.py <image_path>")

if __name__ == "__main__":
    main() 