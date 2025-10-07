#!/usr/bin/env python3
"""
Test client for YOLOv11x backend with static image
Use this to test without webcam
"""

import cv2
import base64
import socketio
import time
import sys

# Configuration
SERVER_URL = "http://localhost:3000"

# Create Socket.IO client
sio = socketio.Client()
result_received = False
detection_result = None

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
    global result_received, detection_result
    detection_result = data
    result_received = True
    print(f"\n[DETECTIONS] Received {data.get('count', 0)} detections")

@sio.event
def error(data):
    """Handle error messages"""
    global result_received
    print(f"[ERROR] {data.get('message', 'Unknown error')}")
    result_received = True

def test_image(image_path):
    """Test with a static image"""
    global result_received, detection_result
    
    print("=" * 70)
    print("YOLOv11x Image Test Client")
    print("=" * 70)
    
    # Read image
    print(f"\nReading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"[ERROR] Could not read image: {image_path}")
        return
    
    print(f"[OK] Image loaded: {image.shape[1]}x{image.shape[0]}")
    
    # Connect to server
    print(f"\nConnecting to server at {SERVER_URL}...")
    try:
        sio.connect(SERVER_URL)
        time.sleep(0.5)  # Wait for connection
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        print("\nMake sure the server is running:")
        print("  1. cd yolov11x-backend")
        print("  2. venv\\Scripts\\activate")
        print("  3. python server.py")
        return
    
    # Encode image
    print("\nEncoding image...")
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
    image_b64 = base64.b64encode(buffer).decode('utf-8')
    
    # Send to server
    print("Sending frame to server...")
    result_received = False
    sio.emit('frame', {'image': image_b64})
    
    # Wait for result
    timeout = 10  # seconds
    start_time = time.time()
    while not result_received and (time.time() - start_time) < timeout:
        time.sleep(0.1)
    
    if not result_received:
        print("[ERROR] Timeout waiting for detection results")
        sio.disconnect()
        return
    
    # Process results
    if detection_result:
        detections = detection_result.get('detections', [])
        count = detection_result.get('count', 0)
        
        print(f"\n{'=' * 70}")
        print(f"DETECTION RESULTS ({count} objects detected)")
        print('=' * 70)
        
        if detections:
            for i, det in enumerate(detections, 1):
                x1, y1, x2, y2 = det['bbox']
                print(f"\n{i}. {det['class_name']}")
                print(f"   Confidence: {det['confidence']:.2%}")
                print(f"   Bounding Box: ({x1:.0f}, {y1:.0f}) -> ({x2:.0f}, {y2:.0f})")
            
            # Draw detections on image
            print("\nDrawing detections on image...")
            for det in detections:
                x1, y1, x2, y2 = map(int, det['bbox'])
                label = f"{det['class_name']}: {det['confidence']:.2f}"
                
                # Draw box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                cv2.putText(image, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Display result
            print("\nDisplaying result... (Press any key to close)")
            cv2.imshow('YOLOv11x Detection Result', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Save result
            output_path = image_path.replace('.', '_detected.')
            cv2.imwrite(output_path, image)
            print(f"\n[SAVED] Result saved to: {output_path}")
        else:
            print("\nNo objects detected in the image.")
    
    # Disconnect
    sio.disconnect()
    print("\n[DONE] Test complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_image.py <path_to_image>")
        print("\nExample:")
        print("  python test_image.py test.jpg")
        sys.exit(1)
    
    test_image(sys.argv[1])

