#!/usr/bin/env python3
# recognize_video4_final.py
# Script cuối cùng để nhận dạng biển số trong video4.mp4

import cv2
import numpy as np
import os
from YOLO_Detection import create_yolo_detector
from OCR_Module_Basic import BasicOCRProcessor

def recognize_video4_final():
    print("🎬 License Plate Recognition in video4.mp4")
    print("=" * 60)
    
    video_path = "models/video4.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    
    # Tạo detector và OCR processor
    detector = create_yolo_detector('models/license_plate_detector.pt')
    ocr_processor = BasicOCRProcessor()
    
    # Mở video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open video file: {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"📹 Video Info:")
    print(f"   Path: {video_path}")
    print(f"   Total Frames: {total_frames}")
    print(f"   FPS: {fps}")
    print(f"   Duration: {total_frames/fps:.2f} seconds")
    
    # Lưu tất cả kết quả nhận dạng
    all_recognition_results = []
    
    print(f"\n🎯 Processing video for license plate recognition...")
    
    for frame_num in range(total_frames):
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Hiển thị tiến độ
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"   Progress: {progress:.1f}% ({frame_num}/{total_frames})")
        
        # YOLO detection
        try:
            detected_plates = detector.detect_license_plates(frame)
            
            for plate in detected_plates:
                confidence = plate['confidence']
                bbox = plate['bbox']
                plate_image = plate['image']
                
                # OCR recognition
                try:
                    ocr_result, ocr_confidence = ocr_processor.recognize_license_plate(plate_image)
                    
                    if ocr_result.strip():  # Chỉ lưu kết quả có text
                        result = {
                            'frame_num': frame_num,
                            'detection_confidence': confidence,
                            'ocr_text': ocr_result,
                            'ocr_confidence': ocr_confidence,
                            'bbox': bbox,
                            'plate_image': plate_image
                        }
                        all_recognition_results.append(result)
                        
                except Exception as e:
                    pass
                    
        except Exception as e:
            pass
    
    cap.release()
    
    # Phân tích kết quả
    print(f"\n📊 Recognition Analysis:")
    print(f"   Total frames processed: {total_frames}")
    print(f"   Total recognitions found: {len(all_recognition_results)}")
    
    if all_recognition_results:
        # Sắp xếp theo OCR confidence
        all_recognition_results.sort(key=lambda x: x['ocr_confidence'], reverse=True)
        
        print(f"\n🏆 Best Recognition Results:")
        
        # Hiển thị top 10 kết quả
        for i, result in enumerate(all_recognition_results[:10]):
            print(f"\n   {i+1}. Frame {result['frame_num']}")
            print(f"      Detection Confidence: {result['detection_confidence']:.2f}")
            print(f"      OCR Text: '{result['ocr_text']}'")
            print(f"      OCR Confidence: {result['ocr_confidence']:.2f}")
            print(f"      Bbox: {result['bbox']}")
            
            # Lưu ảnh biển số tốt nhất
            if i == 0:  # Kết quả tốt nhất
                best_plate_path = "best_recognized_plate.jpg"
                cv2.imwrite(best_plate_path, result['plate_image'])
                print(f"      Saved best plate: {best_plate_path}")
        
        # Thống kê theo text
        text_counts = {}
        for result in all_recognition_results:
            text = result['ocr_text']
            if text in text_counts:
                text_counts[text] += 1
            else:
                text_counts[text] = 1
        
        print(f"\n📈 Text Frequency Analysis:")
        sorted_texts = sorted(text_counts.items(), key=lambda x: x[1], reverse=True)
        
        for text, count in sorted_texts[:5]:
            print(f"   '{text}': {count} times")
        
        # Tìm biển số có khả năng cao nhất
        best_result = all_recognition_results[0]
        print(f"\n🎯 Most Likely License Plate:")
        print(f"   Text: '{best_result['ocr_text']}'")
        print(f"   OCR Confidence: {best_result['ocr_confidence']:.2f}")
        print(f"   Detection Confidence: {best_result['detection_confidence']:.2f}")
        print(f"   Frame: {best_result['frame_num']}")
        
    else:
        print(f"\n❌ No license plates recognized in the video")
    
    return all_recognition_results

def save_recognition_summary(results):
    """Lưu tóm tắt kết quả nhận dạng"""
    if not results:
        return
    
    summary_path = "video4_recognition_summary.txt"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("🎬 License Plate Recognition Summary - video4.mp4\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 Total recognitions found: {len(results)}\n\n")
        
        f.write("🏆 Top Recognition Results:\n")
        for i, result in enumerate(results[:10]):
            f.write(f"\n{i+1}. Frame {result['frame_num']}\n")
            f.write(f"   Detection Confidence: {result['detection_confidence']:.2f}\n")
            f.write(f"   OCR Text: '{result['ocr_text']}'\n")
            f.write(f"   OCR Confidence: {result['ocr_confidence']:.2f}\n")
            f.write(f"   Bbox: {result['bbox']}\n")
        
        # Thống kê text
        text_counts = {}
        for result in results:
            text = result['ocr_text']
            if text in text_counts:
                text_counts[text] += 1
            else:
                text_counts[text] = 1
        
        f.write(f"\n📈 Text Frequency:\n")
        sorted_texts = sorted(text_counts.items(), key=lambda x: x[1], reverse=True)
        for text, count in sorted_texts:
            f.write(f"   '{text}': {count} times\n")
    
    print(f"📄 Summary saved to: {summary_path}")

if __name__ == "__main__":
    print("🎬 License Plate Recognition in video4.mp4")
    print("=" * 60)
    
    # Nhận dạng biển số
    results = recognize_video4_final()
    
    # Lưu tóm tắt
    save_recognition_summary(results)
    
    print(f"\n🎉 Recognition completed!")
    print(f"   Check 'video4_recognition_summary.txt' for detailed results")
    print(f"   Check 'best_recognized_plate.jpg' for the best plate image") 