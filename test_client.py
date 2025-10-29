#!/usr/bin/env python3
"""
Test client for YOLOv11x backend
Captures frames from webcam and sends to server for detection
"""

import cv2
import base64
import socketio
import time
import numpy as np

# Configuration
SERVER_URL = "http://localhost:3000"
CAMERA_ID = 0  # Default webcam
FPS_TARGET = 10  # Target frames per second to send
FRAME_DELAY = 1.0 / FPS_TARGET

# Webcam resolution settings (1:1 aspect ratio)
FRAME_WIDTH = 800
FRAME_HEIGHT = 800

# Detection display settings
BOX_COLOR = (0, 255, 0)  # Green
BOX_THICKNESS = 2
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 1

# Global variables
current_detections = []
detection_count = 0
fps = 0
processing = False

# Create Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    """Handle connection to server"""
    print("[CONNECTED] Successfully connected to server")

@sio.event
def disconnect():
    """Handle disconnection from server"""
    print("[DISCONNECTED] Disconnected from server")

@sio.event
def connection_response(data):
    """Handle connection response"""
    print(f"[SERVER] {data.get('message', 'Connected')}")

@sio.event
def detections(data):
    """Handle detection results from server"""
    global current_detections, detection_count, processing
    current_detections = data.get('detections', [])
    detection_count = data.get('count', 0)
    processing = False
    
    # Print detections with confidence levels
    if detection_count > 0:
        print(f"[DETECTIONS] Received {detection_count} objects (70%+ confidence):")
        for i, det in enumerate(current_detections[:5], 1):  # Show first 5
            print(f"  {i}. {det['class_name']}: {det['confidence']:.1%}")
    else:
        print(f"[DETECTIONS] No objects detected (above 70% threshold)")

@sio.event
def error(data):
    """Handle error messages"""
    global processing
    print(f"[ERROR] {data.get('message', 'Unknown error')}")
    processing = False

def encode_frame(frame, quality=50):
    """Encode frame to base64 JPEG"""
  
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    base64_string = base64.b64encode(buffer).decode('utf-8')
    
  
    return base64_string

def draw_detections(frame, detections):
    """Draw bounding boxes and labels on frame"""
    for det in detections:
        # Get bbox coordinates
        x1, y1, x2, y2 = map(int, det['bbox'])
        confidence = det['confidence']
        class_name = det['class_name']
        
        # Color based on confidence (Green to Yellow)
        # 70-79%: Yellow-green, 80-89%: Light green, 90%+: Bright green
        if confidence >= 0.9:
            color = (0, 255, 0)      # Bright green (90%+)
        elif confidence >= 0.8:
            color = (0, 255, 128)    # Light green (80-89%)
        else:
            color = (0, 200, 255)    # Yellow-green (70-79%)
        
        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, BOX_THICKNESS)
        
        # Prepare label with percentage
        label = f"{class_name}: {confidence:.1%}"  # Show as percentage
        
        # Get label size
        (label_width, label_height), baseline = cv2.getTextSize(
            label, FONT, FONT_SCALE, FONT_THICKNESS
        )
        
        # Draw label background
        cv2.rectangle(
            frame,
            (x1, y1 - label_height - 10),
            (x1 + label_width, y1),
            color,
            -1
        )
        
        # Draw label text
        cv2.putText(
            frame,
            label,
            (x1, y1 - 5),
            FONT,
            FONT_SCALE,
            (0, 0, 0),
            FONT_THICKNESS
        )
    
    return frame

def draw_info(frame, fps, detection_count, processing):
    """Draw information overlay"""
    height, width = frame.shape[:2]
    
    # Draw semi-transparent background for info (adjusted for 500x500 frame)
    overlay = frame.copy()
    # Smaller info box for 500x500 resolution
    info_width = min(280, width - 20)
    info_height = 110
    cv2.rectangle(overlay, (10, 10), (10 + info_width, 10 + info_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Draw text info
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 35), FONT, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"Detections: {detection_count}", (20, 60), FONT, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"Min Confidence: 70%", (20, 85), FONT, 0.6, (100, 200, 255), 1)
    
    status = "Processing..." if processing else "Ready"
    color = (0, 255, 255) if processing else (0, 255, 0)
    cv2.putText(frame, f"Status: {status}", (20, 110), FONT, 0.6, color, 1)
    
    return frame

def main():
    """Main function"""
    global current_detections, detection_count, fps, processing
    
    print("=" * 70)
    print("YOLOv11x Webcam Test Client")
    print("=" * 70)
    
    # Connect to server
    print(f"\nConnecting to server at {SERVER_URL}...")
    try:
        sio.connect(SERVER_URL)
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        print("\nMake sure the server is running:")
        print("  1. cd yolov11x-backend")
        print("  2. venv\\Scripts\\activate")
        print("  3. python server.py")
        return
    
    # Open webcam
    print(f"Opening webcam (ID: {CAMERA_ID})...")
    cap = cv2.VideoCapture(CAMERA_ID)
    
    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        sio.disconnect()
        return
    
    # Set webcam resolution to 500x500 (1:1 aspect ratio)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    # Get actual resolution (webcam may adjust to nearest supported resolution)
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"\n[SUCCESS] Webcam opened successfully!")
    print(f"[INFO] Requested resolution: {FRAME_WIDTH}x{FRAME_HEIGHT} (1:1)")
    print(f"[INFO] Actual resolution: {actual_width}x{actual_height}")
    print(f"[INFO] Target FPS: {FPS_TARGET}")
    print(f"[INFO] Server: {SERVER_URL}")
    print("\nPress 'q' to quit\n")
    
    # FPS calculation
    frame_count = 0
    start_time = time.time()
    last_send_time = 0
    
    try:
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read frame from webcam")
                break
            
            # Resize frame to exactly 500x500 (1:1) if webcam didn't support it
            if frame.shape[1] != FRAME_WIDTH or frame.shape[0] != FRAME_HEIGHT:
                frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT), interpolation=cv2.INTER_LINEAR)
            
            # Calculate FPS
            frame_count += 1
            elapsed = time.time() - start_time
            if elapsed > 1.0:
                fps = frame_count / elapsed
                frame_count = 0
                start_time = time.time()
            
            # Send frame to server at target FPS
            current_time = time.time()
            if current_time - last_send_time >= FRAME_DELAY and not processing:
                processing = True
                frame_b64 = encode_frame(frame)
                sio.emit('frame', {'image': frame_b64})
                last_send_time = current_time
            
            # Draw detections
            if current_detections:
                frame = draw_detections(frame, current_detections)
            
            # Draw info overlay
            frame = draw_info(frame, fps, detection_count, processing)
            
            # Display frame (window will show 500x500 square)
            cv2.imshow('YOLOv11x Live Detection (500x500)', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[INFO] Quitting...")
                break
    
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
    
    finally:
        # Cleanup
        print("[INFO] Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        sio.disconnect()
        print("[INFO] Done!")

if __name__ == "__main__":
    main()

