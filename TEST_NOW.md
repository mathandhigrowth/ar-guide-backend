# 🚀 Test Your Webcam RIGHT NOW!

## Super Simple 2-Step Process

### Step 1: Start Server (Terminal 1)

Open a command prompt and run:

```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python server.py
```

**Wait for this message:**

```
Starting server on 0.0.0.0:3000
```

**Keep this window open!**

---

### Step 2: Start Webcam Test (Terminal 2)

Open a **NEW** command prompt and run:

```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python test_client.py
```

**You should see:**

- Connection success message
- Webcam opens in a new window
- Real-time object detection with green boxes
- FPS and detection count overlay

**Press 'q' to quit the webcam window**

---

## Even Simpler: Use Batch Files

### Option 1: Double-click these files in order:

1. **Double-click** `start_server.bat` (keep it open)
2. **Double-click** `start_webcam_test.bat` (webcam will open)

---

## What You'll See

### Webcam Window:

```
┌─────────────────────────────────┐
│ [Live Webcam Feed]              │
│                                 │
│  ╔════════╗  <- Green box       │
│  ║ Person ║  <- Class name      │
│  ║  0.92  ║  <- Confidence      │
│  ╚════════╝                     │
│                                 │
│ FPS: 8.5                        │
│ Detections: 1                   │
│ Status: Ready                   │
└─────────────────────────────────┘
```

---

## Quick Troubleshooting

### "Could not connect to server"

→ Make sure server (Step 1) is running first!

### "Could not open webcam"

→ Close other apps using webcam (Zoom, Teams, etc.)

### Slow/Low FPS

→ Normal on CPU! Expected: 5-10 FPS
→ For faster inference, use GPU

---

## Don't Have a Webcam? Test with Image Instead!

```bash
python test_image.py path\to\your\image.jpg
```

Example:

```bash
# Download a test image first or use your own
python test_image.py C:\Users\SANJAI\Pictures\photo.jpg
```

---

## Status Check

✅ Server code: `server.py`
✅ Client code: `test_client.py`
✅ Model file: `model/best.pt` (18.3 MB)
✅ All dependencies installed
✅ Ready to test!

---

## Commands Cheat Sheet

### Terminal 1 (Server):

```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python server.py
# Keep running...
```

### Terminal 2 (Client):

```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python test_client.py
# Webcam opens, press 'q' to quit
```

### Stop:

- Server: Press **Ctrl+C** in Terminal 1
- Client: Press **'q'** in webcam window

---

## 🎯 Your Mission

1. Open 2 terminal windows
2. Run server in Terminal 1
3. Run client in Terminal 2
4. Watch live detection on your webcam!
5. Come back and tell me it works! 🎉

Good luck!
