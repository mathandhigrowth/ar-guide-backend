# Testing Instructions for YOLOv11x Backend

## Prerequisites

1. **Server must be running**
   ```bash
   cd yolov11x-backend
   venv\Scripts\activate
   python server.py
   ```
   
2. **Model file present**: `model/best.pt` (already confirmed)

## Option 1: Test with Webcam (Real-time)

### Run the webcam test client:
```bash
python test_client.py
```

### Features:
- Real-time object detection from your webcam
- Live FPS counter
- Detection count display
- Bounding boxes with class names and confidence
- Processing status indicator

### Controls:
- **'q'**: Quit the application

### Troubleshooting:
- If webcam doesn't open, check `CAMERA_ID` in `test_client.py`
- Default is `0` for primary webcam
- Try `1`, `2`, etc. for other cameras

## Option 2: Test with Static Image

### Run the image test client:
```bash
python test_image.py <path_to_image>
```

### Example:
```bash
python test_image.py test_image.jpg
```

### Features:
- Test with any image file
- Displays detections with bounding boxes
- Saves result to `<filename>_detected.<ext>`
- Prints detailed detection results

## Test Flow

### 1. Start Server (Terminal 1)
```bash
cd yolov11x-backend
venv\Scripts\activate
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

### 2. Run Test Client (Terminal 2)
```bash
cd yolov11x-backend
venv\Scripts\activate

# For webcam test:
python test_client.py

# OR for image test:
python test_image.py path/to/image.jpg
```

## Expected Output

### Server Console:
```
Client connected: abc123xyz
Processing frame...
Detections: 3 objects found
```

### Client Console:
```
[CONNECTED] Successfully connected to server
[SERVER] Successfully connected to YOLOv11x server
Opening webcam (ID: 0)...
[SUCCESS] Webcam opened successfully!
[INFO] Target FPS: 10
```

### Client Window:
- Live video feed
- Green bounding boxes around detected objects
- Labels with class name and confidence
- FPS and detection count overlay

## Configuration Options

### test_client.py
```python
SERVER_URL = "http://localhost:3000"  # Server address
CAMERA_ID = 0                         # Webcam ID
FPS_TARGET = 10                       # Frames per second
```

### Adjust FPS:
- Lower FPS (5-7): Better for slower CPUs
- Higher FPS (10-15): Better for GPUs

### Change webcam:
- `CAMERA_ID = 0`: Default webcam
- `CAMERA_ID = 1`: External webcam

## Common Issues

### Issue: "Could not connect to server"
**Solution:**
1. Make sure server is running
2. Check if port 3000 is available
3. Try: `npx kill-port 3000` then restart server

### Issue: "Could not open webcam"
**Solution:**
1. Check if webcam is connected
2. Try different CAMERA_ID (0, 1, 2)
3. Check if another app is using webcam

### Issue: "Model not loaded"
**Solution:**
1. Verify `model/best.pt` exists
2. Check file size (should be > 10 MB)
3. Restart server

### Issue: Slow inference (low FPS)
**Solution:**
1. Lower FPS_TARGET to 5-7
2. Reduce frame size in test_client.py
3. Consider GPU acceleration

## Performance Tips

### CPU Optimization:
- Reduce FPS_TARGET to 5-7
- Resize frames before sending
- Lower JPEG quality (50-70)

### GPU Optimization:
- Install CUDA-enabled PyTorch
- Increase FPS_TARGET to 15-20
- Enable FP16 inference

## Next Steps

After successful testing:
1. ✅ Mark "Test Server Locally" as complete
2. Move to "Integrate with Flutter"
3. Deploy to production server with GPU

## Support

If you encounter issues:
1. Check server logs in Terminal 1
2. Check client output in Terminal 2
3. Verify model file integrity
4. Restart both server and client

