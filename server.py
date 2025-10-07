#!/usr/bin/env python3
"""
YOLOv11x Live Detection Backend Server
Socket.IO server for real-time object detection
"""

import socketio
import uvicorn
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import asyncio
import config  

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=config.CORS_ORIGINS
)

# Create ASGI app
app = socketio.ASGIApp(sio)

# Global model variable
model = None

def load_model():
    """Load YOLOv11x model"""
    global model
    try:
        print("Loading YOLOv11x model...")
        print(f"Model path: {config.MODEL_PATH}")
        model = YOLO(config.MODEL_PATH)
        print(f"✓ Model loaded successfully!")
        print(f"  Model type: {model.type}")
        print(f"\nConfiguration:")
        print(f"  Confidence threshold: {config.YOLO_PARAMS['conf']:.0%}")
        print(f"  IoU threshold: {config.YOLO_PARAMS['iou']}")
        print(f"  Device: {config.DEVICE}")
        print(f"  Preset: {config.ACTIVE_PRESET or 'Custom'}")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure 'model/best.pt' exists in the model directory")
        return False

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    await sio.emit('connection_response', {
        'status': 'connected',
        'message': 'Successfully connected to YOLOv11x server'
    }, to=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")

@sio.event
async def frame(sid, data):
    """
    Handle incoming frame from client
    Expected data format: {
        'image': base64_encoded_image_string
    }
    """
    try:
        if model is None:
            print(f"[ERROR] Model not loaded!")
            await sio.emit('error', {
                'message': 'Model not loaded'
            }, to=sid)
            return
        
        # Decode base64 image
        print(f"[FRAME] Received frame from {sid}")
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            await sio.emit('error', {
                'message': 'Failed to decode image'
            }, to=sid)
            return
        
        # Run YOLO inference with configured parameters
        print(f"[INFERENCE] Running YOLO on frame shape: {frame.shape}")
        results = model(frame, **config.YOLO_PARAMS)
        
        # Extract detections (already filtered by confidence threshold)
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'bbox': box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                    'confidence': float(box.conf[0]),
                    'class_id': int(box.cls[0]),
                    'class_name': model.names[int(box.cls[0])]
                }
                detections.append(detection)
        
        print(f"Detections:{detections}")        
        print(f"[DETECTIONS] Found {len(detections)} objects (conf > {config.YOLO_PARAMS['conf']:.0%})")
        
        # Send detections back to client
        await sio.emit('detections', {
            'detections': detections,
            'count': len(detections)
        }, to=sid)
        print(f"[SENT] Detections sent to {sid}")
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        await sio.emit('error', {
            'message': f'Error processing frame: {str(e)}'
        }, to=sid)

@sio.event
async def ping(sid, data):
    """Handle ping requests for connection testing"""
    await sio.emit('pong', {'timestamp': data.get('timestamp')}, to=sid)

def main():
    """Main function to start the server"""
    print("=" * 70)
    print("YOLOv11x Live Detection Backend Server")
    print("=" * 70)
    
    # Load model
    if not load_model():
        print("\nWarning: Server starting without model loaded.")
        print("Add your model file to 'model/best.pt' and restart.\n")
    
    # Start server
    print(f"\nStarting server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    print("Press CTRL+C to stop\n")
    
    uvicorn.run(
        app,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        log_level="info"
    )

if __name__ == "__main__":
    main()

