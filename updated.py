#!/usr/bin/env python3
"""
YOLOv11x Live Detection Backend Server (Optimized)
Socket.IO server for real-time object detection with persistent IDs
"""

import socketio
import uvicorn
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import asyncio
import config
from collections import deque
import uuid
import time
import threading

# -------------------------------
# Socket.IO server
# -------------------------------
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=config.CORS_ORIGINS)

app = socketio.ASGIApp(sio)

# -------------------------------
# Global variables
# -------------------------------
model = None
object_tracker = {}  # {unique_id: last_seen_timestamp}


# -------------------------------
# Load YOLO model
# -------------------------------
def load_model():
    global model
    try:
        print("Loading YOLOv11x model...")
        print(f"Model path: {config.MODEL_PATH}")
        model = YOLO(config.MODEL_PATH)
        print(f"✓ Model loaded successfully! Type: {model.type}")
        print(f"Confidence threshold: {config.YOLO_PARAMS['conf']}")
        print(f"IoU threshold: {config.YOLO_PARAMS['iou']}")
        print(f"Device: {config.DEVICE}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return False


# -------------------------------
# Helper: Resize frame for bandwidth
# -------------------------------
def preprocess_frame(frame, max_dim=640):
    h, w = frame.shape[:2]
    scale = max_dim / max(h, w)
    if scale < 1.0:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
    return frame


# -------------------------------
# Persistent ID generator
# -------------------------------
def get_persistent_id():
    return str(uuid.uuid4())


# -------------------------------
# Handle client connection
# -------------------------------
@sio.event
async def connect(sid, environ):
    print(f"[CONNECT] Client connected: {sid}")
    await sio.emit(
        "connection_response",
        {"status": "connected", "message": "Successfully connected to YOLOv11x server"},
        to=sid,
    )


@sio.event
async def disconnect(sid):
    print(f"[DISCONNECT] Client disconnected: {sid}")


# -------------------------------
# Process incoming frames
# -------------------------------
@sio.event
async def frame(sid, data):
    """
    Expected data:
    {
        'image': base64_encoded_image
    }
    """
    try:
        if model is None:
            await sio.emit("error", {"message": "Model not loaded"}, to=sid)
            return

        # Decode frame
        image_data = base64.b64decode(data["image"])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            await sio.emit("error", {"message": "Failed to decode image"}, to=sid)
            return

        # Resize to reduce bandwidth / inference time
        frame = preprocess_frame(frame, max_dim=config.FRAME_MAX_DIM)
        h, w = frame.shape[:2]

        # -------------------------------
        # Run YOLO inference asynchronously
        # -------------------------------
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None, lambda: model(frame, **config.YOLO_PARAMS)
        )

        detections = []
        current_time = time.time()

        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]

                # Assign persistent ID
                unique_id = get_persistent_id()

                detections.append(
                    {
                        "id": unique_id,
                        "bbox": bbox,
                        "confidence": float(box.conf[0]),
                        "class_id": class_id,
                        "class_name": label,
                    }
                )

                # Track last seen timestamp
                object_tracker[unique_id] = current_time

        # Send detections to Flutter client
        await sio.emit(
            "detections",
            {
                "detections": detections,
                "count": len(detections),
                "frame_size": {"width": w, "height": h},  # for coordinate mapping
            },
            to=sid,
        )

    except Exception as e:
        print(f"[ERROR] Failed processing frame: {e}")
        await sio.emit(
            "error", {"message": f"Error processing frame: {str(e)}"}, to=sid
        )


# -------------------------------
# Ping/Pong for latency testing
# -------------------------------
@sio.event
async def ping(sid, data):
    await sio.emit("pong", {"timestamp": data.get("timestamp")}, to=sid)


# -------------------------------
# Cleanup old tracked objects
# -------------------------------
def cleanup_old_objects(max_age_seconds=5):
    while True:
        now = time.time()
        to_remove = [
            uid for uid, t in object_tracker.items() if now - t > max_age_seconds
        ]
        for uid in to_remove:
            del object_tracker[uid]
        time.sleep(1)


# -------------------------------
# Main server entry point
# -------------------------------
def main():
    print("=" * 70)
    print("YOLOv11x Live Detection Backend Server (Optimized)")
    print("=" * 70)

    if not load_model():
        print("[WARNING] Server starting without a model loaded.")

    # Start object cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_objects, daemon=True)
    cleanup_thread.start()

    # Start server
    print(f"\nStarting server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    print("Press CTRL+C to stop\n")

    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT, log_level="info")


if __name__ == "__main__":
    main()
