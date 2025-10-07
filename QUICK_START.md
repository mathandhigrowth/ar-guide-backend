# Quick Start Guide - Testing with Webcam

## Step-by-Step Instructions

### Step 1: Start the Server

**Option A: Using batch file (Easiest)**
1. Double-click `start_server.bat`
2. Wait for "Starting server on 0.0.0.0:3000" message

**Option B: Using command line**
1. Open a terminal/command prompt
2. Run:
   ```bash
   cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
   python server.py
   ```

You should see:
```
============================================================
YOLOv11x Live Detection Backend Server
============================================================
Loading YOLOv11x model...
Model loaded successfully!

Starting server on 0.0.0.0:3000
Press CTRL+C to stop
```

**IMPORTANT: Keep this terminal window open!**

---

### Step 2: Start the Webcam Test Client

**Option A: Using batch file (Easiest)**
1. Double-click `start_webcam_test.bat`
2. A window will open showing your webcam feed with detections

**Option B: Using command line**
1. Open a **NEW** terminal/command prompt (keep server running)
2. Run:
   ```bash
   cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
   python test_client.py
   ```

You should see:
```
======================================================================
YOLOv11x Webcam Test Client
======================================================================

Connecting to server at http://localhost:3000...
[CONNECTED] Successfully connected to server
[SERVER] Successfully connected to YOLOv11x server
Opening webcam (ID: 0)...
[SUCCESS] Webcam opened successfully!
```

A window titled "YOLOv11x Live Detection" will open showing:
- Live webcam feed
- Green bounding boxes around detected objects
- Labels with class names and confidence scores
- FPS counter
- Detection count
- Processing status

---

### Step 3: Test It!

- Move objects in front of your webcam
- Watch as the model detects them in real-time
- Green boxes will appear around detected objects
- Press **'q'** to quit

---

## Troubleshooting

### Problem: "Could not connect to server"
- Make sure Step 1 (server) is running first
- Check the server terminal for error messages
- Try: `npx kill-port 3000` then restart server

### Problem: "Could not open webcam"
- Check if your webcam is connected
- Close other apps using the webcam (Zoom, Teams, etc.)
- Edit `test_client.py` and change `CAMERA_ID = 0` to `CAMERA_ID = 1`

### Problem: Low FPS / Slow performance
- This is normal on CPU (you're running without GPU)
- Expected FPS: 5-10 on CPU
- For better performance, install CUDA + GPU-enabled PyTorch

### Problem: No detections showing
- Make sure there are objects in frame that the model was trained on
- Check detection confidence threshold
- Verify model loaded correctly in server terminal

---

## Alternative: Test with Image Instead

If webcam doesn't work, test with a static image:

```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python test_image.py path\to\your\image.jpg
```

This will:
1. Connect to server
2. Send the image for detection
3. Display results
4. Save annotated image

---

## What You Should See

### Server Terminal:
```
Client connected: xyz123
INFO:     127.0.0.1:12345 - "POST /socket.io/ HTTP/1.1" 200 OK
```

### Client Window:
- Live video feed from your webcam
- FPS: ~5-10 (on CPU)
- Detections: X objects
- Status: Ready / Processing...
- Green bounding boxes with labels

---

## Next Steps After Successful Test

1. ✅ Mark "5. Test Server Locally" as complete in Todo.md
2. Move to "6. Integrate with Flutter"
3. Build Flutter app with socket_io_client
4. Deploy to GPU server for better performance

---

## Commands Summary

### Terminal 1 (Server):
```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python server.py
```

### Terminal 2 (Client):
```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python test_client.py
```

### Stop Everything:
- Press **Ctrl+C** in server terminal
- Press **'q'** in client window
- Press **Ctrl+C** in client terminal (if needed)

