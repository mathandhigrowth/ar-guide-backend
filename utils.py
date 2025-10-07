#!/usr/bin/env python3
"""
Utility functions for YOLOv11x backend
Helper functions for image processing, data conversion, etc.
"""

import cv2
import numpy as np
import base64
from typing import List, Dict, Tuple

def resize_frame(frame: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    """
    Resize frame to target size while maintaining aspect ratio
    
    Args:
        frame: Input frame (numpy array)
        target_size: Target size (width, height)
    
    Returns:
        Resized frame
    """
    return cv2.resize(frame, target_size, interpolation=cv2.INTER_LINEAR)

def encode_image_to_base64(frame: np.ndarray, quality: int = 85) -> str:
    """
    Encode numpy array image to base64 string
    
    Args:
        frame: Input frame (numpy array)
        quality: JPEG quality (1-100)
    
    Returns:
        Base64 encoded string
    """
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return base64.b64encode(buffer).decode('utf-8')

def decode_base64_to_image(base64_string: str) -> np.ndarray:
    """
    Decode base64 string to numpy array image
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        Decoded image as numpy array
    """
    image_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def filter_detections_by_confidence(
    detections: List[Dict],
    min_confidence: float = 0.5
) -> List[Dict]:
    """
    Filter detections by minimum confidence threshold
    
    Args:
        detections: List of detection dictionaries
        min_confidence: Minimum confidence threshold (0-1)
    
    Returns:
        Filtered list of detections
    """
    return [d for d in detections if d['confidence'] >= min_confidence]

def filter_detections_by_class(
    detections: List[Dict],
    class_names: List[str]
) -> List[Dict]:
    """
    Filter detections by specific class names
    
    Args:
        detections: List of detection dictionaries
        class_names: List of class names to keep
    
    Returns:
        Filtered list of detections
    """
    return [d for d in detections if d['class_name'] in class_names]

def calculate_iou(box1: List[float], box2: List[float]) -> float:
    """
    Calculate Intersection over Union (IoU) between two bounding boxes
    
    Args:
        box1: First box [x1, y1, x2, y2]
        box2: Second box [x1, y1, x2, y2]
    
    Returns:
        IoU value (0-1)
    """
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    # Calculate intersection area
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return 0.0
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Calculate union area
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0

def apply_nms(
    detections: List[Dict],
    iou_threshold: float = 0.45
) -> List[Dict]:
    """
    Apply Non-Maximum Suppression to remove overlapping detections
    
    Args:
        detections: List of detection dictionaries
        iou_threshold: IoU threshold for suppression
    
    Returns:
        Filtered list of detections after NMS
    """
    if not detections:
        return []
    
    # Sort by confidence (descending)
    sorted_detections = sorted(detections, key=lambda x: x['confidence'], reverse=True)
    
    keep = []
    while sorted_detections:
        current = sorted_detections.pop(0)
        keep.append(current)
        
        # Remove overlapping boxes
        sorted_detections = [
            det for det in sorted_detections
            if calculate_iou(current['bbox'], det['bbox']) < iou_threshold
        ]
    
    return keep

def draw_detections(
    frame: np.ndarray,
    detections: List[Dict],
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw bounding boxes and labels on frame
    
    Args:
        frame: Input frame
        detections: List of detection dictionaries
        color: Box color (B, G, R)
        thickness: Box thickness
    
    Returns:
        Frame with drawn detections
    """
    frame_copy = frame.copy()
    
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        label = f"{det['class_name']}: {det['confidence']:.2f}"
        
        # Draw box
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, thickness)
        
        # Draw label background
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(
            frame_copy,
            (x1, y1 - label_size[1] - 10),
            (x1 + label_size[0], y1),
            color,
            -1
        )
        
        # Draw label text
        cv2.putText(
            frame_copy,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1
        )
    
    return frame_copy

def get_detection_statistics(detections: List[Dict]) -> Dict:
    """
    Calculate statistics from detections
    
    Args:
        detections: List of detection dictionaries
    
    Returns:
        Dictionary with detection statistics
    """
    if not detections:
        return {
            'total_count': 0,
            'class_counts': {},
            'average_confidence': 0.0
        }
    
    class_counts = {}
    total_confidence = 0.0
    
    for det in detections:
        class_name = det['class_name']
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
        total_confidence += det['confidence']
    
    return {
        'total_count': len(detections),
        'class_counts': class_counts,
        'average_confidence': total_confidence / len(detections)
    }

