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

# Global variables
model = None
client_sockets = {}  # Track client types by socket ID

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
    global client_sockets
    
    user_agent = environ.get('HTTP_USER_AGENT', 'Unknown')
    
    # Detect client type from User-Agent or connection path
    if 'Python' in user_agent or 'python' in user_agent.lower():
        client_type = "PYTHON"
    elif 'Dart' in user_agent or 'dart' in user_agent.lower() or 'Flutter' in user_agent:
        client_type = "FLUTTER"
    else:
        # Check path/transport info
        path = environ.get('PATH_INFO', '')
        if 'flutter' in path.lower():
            client_type = "FLUTTER"
        else:
            client_type = "UNKNOWN"
    
    # Store client type for this socket
    client_sockets[sid] = client_type
    
    print(f"[{client_type}] Client connected: {sid}")
    print(f"[{client_type}] User-Agent: {user_agent}")
    
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
        
        # Detect client type from stored socket info
        global client_sockets
        base64_length = len(data['image'])
        
        # Get client type from stored socket info (set during connect event)
        client_type = client_sockets.get(sid, "UNKNOWN")
        
        # If not found, try to identify from base64 size as fallback
        if client_type == "UNKNOWN":
            if base64_length < 15000:
                client_type = "PYTHON"
            else:
                client_type = "FLUTTER"
            client_sockets[sid] = client_type
            print(f"[CLIENT IDENTIFICATION] ✨ Fallback detection: {sid[:15]}... → {client_type}")
        
        import time
        timestamp = time.strftime('%H:%M:%S')
        
        print(f"\n{'='*70}")
        print(f"[{client_type} REQUEST] Socket ID: {sid}")
        print(f"[{client_type} REQUEST] Timestamp: {timestamp}")
        print(f"[{client_type} REQUEST] Base64 length: {base64_length} chars")
        print(f"{'='*70}")
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        print(f"[{sid[:10]}] [{client_type}] 📥 Received frame")
        print(f"[{sid[:10]}] [{client_type}] Base64: {len(data['image'])} chars → Decoded: {len(image_data)} bytes")
        print(f"[{sid[:10]}] [{client_type}] Preview: {data['image'][:50]}...")
        
        # 🔹 Detect format: YUV420 (raw) or JPEG  
        # Note: YUV420 raw is 3x larger than JPEG - not recommended for production
        # Keeping support for both formats for flexibility
        format_type = data.get('format', 'jpeg')  # Default to JPEG (recommended)
        
        if format_type == 'yuv420':
            # YUV420 raw format received
            print(f"[{client_type} FRAME] Format: YUV420 (raw)")
            width = data.get('width')
            height = data.get('height')
            
            if width is None or height is None:
                print(f"[FRAME] ERROR: YUV420 requires width and height parameters")
                await sio.emit('error', {
                    'message': 'YUV420 format requires width and height parameters'
                }, to=sid)
                return
            
            # Decode YUV420 to BGR
            yuv_frame = image_data
            frame = cv2.cvtColor(yuv_frame.reshape((height, width)), cv2.COLOR_YUV420p2BGR)
            # Reshape if needed for YUV420 planes
            
            print(f"[{client_type} FRAME] ✓ Decoded YUV420 to BGR")
        else:
            # JPEG format (default)
            print(f"[{client_type} FRAME] Format: JPEG")
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                print(f"[FRAME] ERROR: Failed to decode image!")
                print(f"[FRAME] First 50 bytes: {image_data[:50]}")
                print(f"[FRAME] Is JPEG header? {image_data[:3] == b'\\xff\\xd8\\xff'}")
                await sio.emit('error', {
                    'message': 'Failed to decode image'
                }, to=sid)
                return
            
            # 🔹 BACKEND CONVERSION OPTION (Python-powered!)
            # Both clients send BGR, but if needed we can force conversion
            # For debugging: check if colors look wrong and manually convert
            needs_conversion = data.get('force_rgb', False)  # Optional flag from client
            
            if needs_conversion and client_type == "FLUTTER":
                # Force Python conversion: RGB→BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                print(f"[{client_type} FRAME] 🔄 Python converted RGB→BGR")
            else:
                # Both clients now send BGR directly
                print(f"[{client_type} FRAME] ✓ Already in BGR format (ready for YOLO)")
        
        # ============================================================
        # ORIENTATION: Keep native portrait (no rotation)
        # ============================================================
        height, width = frame.shape[:2]
        orientation = "portrait" if height > width else "landscape"
        print(f"[{client_type} ORIENTATION] 📸 Input frame: {width}×{height} ({orientation})")
        print(f"[{client_type} ORIENTATION] ✅ Using native orientation (no rotation)")
        
        # Run YOLO inference with configured parameters
        print(f"\n[{sid[:10]}] [{client_type}] 📊 Frame processed:")
        print(f"[{sid[:10]}]    Shape: {frame.shape}")
        print(f"[{sid[:10]}]    Dtype: {frame.dtype}")
        print(f"[{sid[:10]}]    Pixel range: min={frame.min()}, max={frame.max()}")
        print(f"[{sid[:10]}]    Mean brightness: {frame.mean():.1f}")
        
        print(f"\n[{sid[:10]}] [{client_type}] 🔍 Running YOLO inference...")
        results = model(frame, **config.YOLO_PARAMS)
        print(f"[{sid[:10]}] [{client_type}] ✅ Inference completed")
        
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
        
        # 🔹 SINGLE OBJECT MODE: Select only the highest confidence detection
        original_count = len(detections)
        if detections:
            # Sort by confidence (highest first) and take only the first one
            detections = sorted(detections, key=lambda x: x['confidence'], reverse=True)
            detections = detections[:1]  # Keep only the highest confidence detection (slice to ensure single item)
            print(f"[{sid[:10]}] [{client_type}] 🔄 Filtered from {original_count} to {len(detections)} object(s)")
        
        print(f"\n[{sid[:10]}] [{client_type}] 🎯 Detection Results:")
        print(f"[{sid[:10]}]    Found: {len(detections)} object(s)")
        
        if detections:
            det = detections[0]
            print(f"[{sid[:10]}]    🎯 Selected: {det['class_name']} (confidence: {det['confidence']:.1%})")
            print(f"[{sid[:10]}]    Bounding Box: {det['bbox']}")
        else:
            print(f"[{sid[:10]}]    ❌ NO OBJECTS DETECTED!")
        
        print(f"[{sid[:10]}] [{client_type}] 📤 Sending response to client...")
        
        # Send detections back to client (only one object)
        await sio.emit('detections', {
            'detections': detections,
            'count': len(detections)
        }, to=sid)
        
        print(f"[{sid[:10]}] [{client_type}] ✅ Response sent successfully")
        print(f"{'='*70}\n")
        
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

