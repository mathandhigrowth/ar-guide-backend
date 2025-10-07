#!/usr/bin/env python3
"""
All-in-one script to test YOLOv11x with webcam
Starts server in background and runs webcam client
"""

import subprocess
import time
import sys
import os

print("=" * 70)
print("YOLOv11x All-in-One Webcam Test")
print("=" * 70)

# Start server in background
print("\n[1/3] Starting server...")
try:
    if os.name == 'nt':  # Windows
        server_process = subprocess.Popen(
            ['python', 'server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:  # Linux/Mac
        server_process = subprocess.Popen(
            ['python3', 'server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    print("[OK] Server starting in background...")
    print("[INFO] Waiting 5 seconds for server to initialize...")
    time.sleep(5)
    
except Exception as e:
    print(f"[ERROR] Could not start server: {e}")
    sys.exit(1)

# Check if server is running
print("\n[2/3] Checking server connection...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 3000))
sock.close()

if result == 0:
    print("[OK] Server is running on port 3000")
else:
    print("[ERROR] Server is not responding on port 3000")
    print("[INFO] Check if port is already in use: npx kill-port 3000")
    server_process.terminate()
    sys.exit(1)

# Run webcam test client
print("\n[3/3] Starting webcam test client...")
print("[INFO] Press 'q' in the webcam window to quit")
print("=" * 70)
print()

try:
    subprocess.run(['python', 'test_client.py'])
except KeyboardInterrupt:
    print("\n[INFO] Test interrupted by user")
except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    # Cleanup
    print("\n[CLEANUP] Stopping server...")
    server_process.terminate()
    server_process.wait()
    print("[DONE] All processes stopped")

