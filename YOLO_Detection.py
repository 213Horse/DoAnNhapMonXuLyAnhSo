#!/usr/bin/env python3
# YOLO_Detection.py
# Module YOLO để phát hiện biển số xe

import cv2
import numpy as np
from ultralytics import YOLO
import os

class YOLOLicensePlateDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Khởi tạo YOLO License Plate Detector
        
        Args:
            model_path: Đường dẫn đến model YOLO
        """
        try:
            # Load YOLO model
            self.model = YOLO(model_path)
            print(f"✅ YOLO model loaded: {model_path}")
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            self.model = None
    
    def detect_license_plates(self, img):
        """
        Phát hiện biển số xe trong ảnh
        
        Args:
            img: Ảnh đầu vào (numpy array)
            
        Returns:
            List các vùng biển số xe được cắt
        """
        if self.model is None:
            print("❌ YOLO model not loaded")
            return []
        
        try:
            # Dự đoán với YOLO
            results = self.model(img)
            
            detected_plates = []
            
            # Xử lý kết quả
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        # Lấy tọa độ bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        print(f"🔍 Detected plate: ({x1}, {y1}) to ({x2}, {y2}), confidence: {confidence:.2f}")
                        
                        # Cắt vùng biển số
                        plate_img = img[y1:y2, x1:x2]
                        
                        if plate_img.size > 0:  # Kiểm tra ảnh không rỗng
                            detected_plates.append({
                                'image': plate_img,
                                'bbox': (x1, y1, x2, y2),
                                'confidence': confidence,
                                'class_id': class_id
                            })
            
            print(f"✅ Found {len(detected_plates)} license plates")
            return detected_plates
            
        except Exception as e:
            print(f"❌ Error in YOLO detection: {e}")
            return []
    
    def detect_and_show(self, img_path):
        """
        Phát hiện biển số xe và hiển thị kết quả
        
        Args:
            img_path: Đường dẫn đến ảnh
        """
        if not os.path.exists(img_path):
            print(f"❌ Image not found: {img_path}")
            return
        
        # Đọc ảnh
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ Cannot read image: {img_path}")
            return
        
        print(f"📸 Processing image: {img_path}")
        print(f"   Image size: {img.shape}")
        
        # Phát hiện biển số
        detected_plates = self.detect_license_plates(img)
        
        # Hiển thị kết quả
        for i, plate_info in enumerate(detected_plates):
            plate_img = plate_info['image']
            bbox = plate_info['bbox']
            confidence = plate_info['confidence']
            
            print(f"   Plate {i+1}: bbox={bbox}, confidence={confidence:.2f}")
            
            # Hiển thị ảnh biển số
            cv2.imshow(f"Plate {i+1}", plate_img)
            
            # Vẽ bounding box trên ảnh gốc
            x1, y1, x2, y2 = bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"Plate {i+1}: {confidence:.2f}", 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Hiển thị ảnh gốc với bounding boxes
        cv2.imshow("Original with Detections", img)
        
        print(f"✅ Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return detected_plates

def create_yolo_detector(model_path='models/license_plate_detector.pt'):
    """
    Tạo YOLO detector với model chuyên biệt cho biển số xe
    
    Args:
        model_path: Đường dẫn đến model YOLO chuyên biệt
        
    Returns:
        YOLOLicensePlateDetector instance
    """
    return YOLOLicensePlateDetector(model_path)

def test_yolo_detection():
    """Test YOLO detection"""
    print("🧪 Test YOLO License Plate Detection")
    print("=" * 40)
    
    # Tạo detector
    detector = create_yolo_detector()
    
    # Test với ảnh
    img_path = "LicPlateImages/vn1.jpg"
    
    if os.path.exists(img_path):
        detector.detect_and_show(img_path)
    else:
        print(f"❌ Test image not found: {img_path}")

if __name__ == "__main__":
    test_yolo_detection() 