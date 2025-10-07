#!/usr/bin/env python3
"""
Quick connection test for Socket.IO server
Tests if the server is responding correctly
"""

import socketio
import time
import base64
import cv2
import numpy as np

print("=" * 70)
print("Socket.IO Connection Test")
print("=" * 70)

# Create client
sio = socketio.Client()
received_response = False

@sio.event
def connect():
    print("[OK] Connected to server")

@sio.event
def disconnect():
    print("[INFO] Disconnected from server")

@sio.event
def connection_response(data):
    print(f"[OK] Server says: {data.get('message')}")

@sio.event
def detections(data):
    global received_response
    print(f"[OK] Received detections: {data.get('count', 0)} objects")
    if data.get('detections'):
        for i, det in enumerate(data['detections'][:3], 1):  # Show first 3
            print(f"  {i}. {det['class_name']}: {det['confidence']:.2%}")
    received_response = True

@sio.event
def error(data):
    print(f"[ERROR] {data.get('message')}")

# Test
try:
    print("\n[TEST 1] Connecting to server...")
    sio.connect('http://localhost:3000')
    time.sleep(1)
    
    print("\n[TEST 2] Sending test frame...")
    # Create a simple test image (black 640x640)
    test_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    _, buffer = cv2.imencode('.jpg', test_frame)
    frame_b64 = base64.b64encode(buffer).decode('utf-8')
    
    sio.emit('frame', {'image': frame_b64})
    
    print("[INFO] Waiting for response...")
    timeout = 10
    start = time.time()
    while not received_response and (time.time() - start) < timeout:
        time.sleep(0.1)
    
    if received_response:
        print("\n" + "=" * 70)
        print("[SUCCESS] All tests passed! Server is working correctly.")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("[WARNING] No response received within timeout")
        print("Check server logs for errors")
        print("=" * 70)
    
    sio.disconnect()
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    print("\nMake sure server is running:")
    print("  python server.py")

