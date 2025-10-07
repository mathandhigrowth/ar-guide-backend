#!/usr/bin/env python3
"""
Setup and start YOLOv11x server with ngrok tunnel
Makes the server accessible globally via public URL
"""

import subprocess
import time
import sys
import os
import json
import requests

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ ngrok is installed: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("✗ ngrok is not installed")
    return False

def install_ngrok():
    """Guide user to install ngrok"""
    print("\n" + "=" * 70)
    print("ngrok Installation Required")
    print("=" * 70)
    print("\nOption 1: Download from website (Recommended)")
    print("  1. Visit: https://ngrok.com/download")
    print("  2. Download ngrok for Windows")
    print("  3. Extract to a folder")
    print("  4. Add to PATH or run from extracted location")
    
    print("\nOption 2: Using Chocolatey (if installed)")
    print("  choco install ngrok")
    
    print("\nOption 3: Using pip")
    print("  pip install pyngrok")
    
    print("\nAfter installation, get your auth token:")
    print("  1. Sign up at: https://dashboard.ngrok.com/signup")
    print("  2. Get your token at: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("  3. Run: ngrok authtoken YOUR_TOKEN")
    
    print("\n" + "=" * 70)

def get_ngrok_tunnels():
    """Get active ngrok tunnels"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('tunnels', [])
    except:
        pass
    return []

def start_server_with_ngrok():
    """Start server and create ngrok tunnel"""
    print("=" * 70)
    print("YOLOv11x Server with ngrok")
    print("=" * 70)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        install_ngrok()
        print("\nPlease install ngrok and run this script again.")
        return
    
    print("\n[1/3] Starting YOLOv11x server...")
    # Start server in background
    server_process = subprocess.Popen(
        [sys.executable, 'server.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    print("✓ Server starting... (waiting 5 seconds)")
    time.sleep(5)
    
    print("\n[2/3] Starting ngrok tunnel...")
    # Start ngrok
    ngrok_process = subprocess.Popen(
        ['ngrok', 'http', '3000', '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    print("✓ ngrok tunnel starting... (waiting 3 seconds)")
    time.sleep(3)
    
    print("\n[3/3] Getting public URL...")
    # Get tunnel URL
    tunnels = get_ngrok_tunnels()
    
    if tunnels:
        public_url = tunnels[0].get('public_url', 'N/A')
        print("\n" + "=" * 70)
        print("✓ Server is now accessible globally!")
        print("=" * 70)
        print(f"\nPublic URL: {public_url}")
        print(f"Local URL:  http://localhost:3000")
        print("\nShare the public URL with anyone to access your server!")
        print("\nngrok Web Interface: http://localhost:4040")
        print("  (View requests, replay, inspect traffic)")
        
        print("\n" + "=" * 70)
        print("Connection Instructions:")
        print("=" * 70)
        print(f"\nFor test_client.py, update SERVER_URL:")
        print(f'  SERVER_URL = "{public_url}"')
        
        print(f"\nFor Flutter app, use:")
        print(f'  socket_io_client.connect("{public_url}");')
        
        print("\n" + "=" * 70)
        print("\nPress Ctrl+C to stop both server and ngrok tunnel")
        print("=" * 70)
        
        try:
            # Keep running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping server and ngrok tunnel...")
            server_process.terminate()
            ngrok_process.terminate()
            print("✓ Stopped")
    else:
        print("\n✗ Could not get ngrok tunnel URL")
        print("Please check:")
        print("  1. ngrok is authenticated: ngrok authtoken YOUR_TOKEN")
        print("  2. Port 3000 is not in use")
        print("  3. ngrok dashboard: http://localhost:4040")
        
        server_process.terminate()
        ngrok_process.terminate()

if __name__ == "__main__":
    try:
        start_server_with_ngrok()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTry manual setup:")
        print("  Terminal 1: python server.py")
        print("  Terminal 2: ngrok http 3000")

