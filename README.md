# YOLOv11x Live Detection Backend

A Socket.IO server for real-time object detection using YOLOv11x model.

## Setup Complete ✓

### Environment Details

- **Python Version**: 3.13.7
- **PyTorch Version**: 2.8.0+cpu
- **Device**: CPU (CUDA not available)

### Installed Packages

- ✓ Ultralytics 8.3.204
- ✓ Python-SocketIO
- ✓ Uvicorn
- ✓ OpenCV 4.12.0
- ✓ NumPy 2.2.6
- ✓ PyTorch 2.8.0+cpu

## Project Structure

```
yolov11x-backend/
├── server.py             # Main Socket.IO server ✓
├── model/
│   ├── best.pt           # Trained YOLOv11x weights (add your model here)
│   └── README.md         # Model directory instructions ✓
├── utils.py              # Helper functions ✓
├── requirements.txt      # Python dependencies ✓
├── Dockerfile            # Docker deployment config ✓
├── .dockerignore         # Docker ignore patterns ✓
├── .gitignore            # Git ignore patterns ✓
└── README.md             # This file ✓
```

## Getting Started

### 1. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Test Setup

```bash
python test_setup.py
```

### 3. Add Your Model

Place your trained YOLOv11x weights file (`best.pt`) in the `model/` directory.

### 4. Run Server

```bash
python server.py
```

The server will start on `http://0.0.0.0:3000`

## Available Features

### Server (server.py)

- Socket.IO async server with CORS support
- Real-time frame processing
- YOLOv11x inference
- Connection management
- Error handling

### Socket.IO Events

**Client → Server:**

- `connect` - Establish connection
- `frame` - Send frame for detection (expects base64 encoded image)
- `ping` - Connection test
- `disconnect` - Close connection

**Server → Client:**

- `connection_response` - Connection confirmation
- `detections` - Detection results (bbox, confidence, class)
- `error` - Error messages
- `pong` - Ping response

### Utilities (utils.py)

- Image resizing and encoding
- Base64 conversion
- Detection filtering by confidence/class
- Non-Maximum Suppression (NMS)
- IoU calculation
- Bounding box drawing
- Detection statistics

## Docker Deployment

### Build Image

```bash
docker build -t yolov11x-backend .
```

### Run Container (GPU)

```bash
docker run --gpus all -p 3000:3000 yolov11x-backend
```

### Run Container (CPU)

```bash
docker run -p 3000:3000 yolov11x-backend
```

## Notes

- Currently running on CPU. For GPU acceleration:
  - Install CUDA-enabled PyTorch
  - Ensure compatible NVIDIA GPU drivers are installed
- CPU inference will work but will be slower than GPU
- Recommended for production: Use a GPU instance for real-time detection

## Global Access with ngrok 🌐

Make your server accessible from anywhere in the world:

### Quick Setup:

```bash
# 1. Install ngrok: https://ngrok.com/download
# 2. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
ngrok authtoken YOUR_TOKEN

# 3. Start with ngrok (Easy)
python setup_ngrok.py
# OR
start_with_ngrok.bat
```

### Manual Setup:

```bash
# Terminal 1: Start server
python server.py

# Terminal 2: Start ngrok tunnel
ngrok http 3000
```

### Your Public URL:

```
https://abc123-45-67-89.ngrok-free.app
```

**Monitor at:** http://localhost:4040

**Full Guide:** See `NGROK_SETUP.md` for complete documentation

---

## Next Steps

- [x] Server implemented with YOLOv11x inference
- [x] Socket.IO event handlers configured
- [x] 70% confidence threshold applied
- [x] Test scripts created
- [x] ngrok setup for global access
- [ ] Test with sample images
- [ ] Integrate with Flutter frontend
- [ ] Test from mobile device via ngrok
- [ ] Deploy to GPU-enabled server

## Contact

For issues or questions, refer to the main project documentation.
