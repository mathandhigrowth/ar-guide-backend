#!/usr/bin/env python3
"""
YOLOv11x Detection Client - PORTRAIT VIEW ONLY (Upright)
Displays camera feed in portrait orientation (9:16) — like a smartphone.
No rotation, no stretch, and no excessive zoom.
"""

import cv2
import base64
import socketio
import time
import numpy as np
from typing import Tuple, Dict

# =====================================================
# Configuration
# =====================================================
SERVER_URL = "http://localhost:3000"
CAMERA_ID = 0

# YOLO input dimensions (portrait 9:16)
YOLO_WIDTH = 640
YOLO_HEIGHT = 1136

# Target FPS
FPS_TARGET = 10
FRAME_DELAY = 1.0 / FPS_TARGET

WINDOW_NAME = "YOLOv11x Portrait Detection"

# =====================================================
# Global state
# =====================================================
sio = socketio.Client()
current_detections = []
detection_count = 0
processing = False
last_transform: Dict = {}

# =====================================================
# Socket.IO events
# =====================================================
@sio.event
def connect():
    print("=" * 60)
    print("[CONNECTED] to YOLO backend")
    print("[MODE] PORTRAIT VIEW ONLY (upright)")
    print(f"[CONFIG] YOLO input: {YOLO_WIDTH}×{YOLO_HEIGHT}")
    print("=" * 60)

@sio.event
def disconnect():
    print("[DISCONNECTED] from server")

@sio.event
def detections(data):
    global current_detections, detection_count, processing
    current_detections = data.get("detections", []) or []
    detection_count = data.get("count", 0) or len(current_detections)
    processing = False

@sio.event
def error(data):
    global processing
    print(f"[ERROR] {data.get('message')}")
    processing = False

# =====================================================
# Helpers
# =====================================================
def encode_frame(frame: np.ndarray, quality: int = 80) -> str:
    """Encode frame as JPEG base64 string."""
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return base64.b64encode(buf).decode("utf-8")

def rotate_to_portrait(frame: np.ndarray) -> np.ndarray:
    """
    Mirror horizontally (selfie-style) and crop to 9:16 portrait view.
    No rotation, no stretch, no padding — true portrait fill.
    """
    mirrored = cv2.flip(frame, 1)
    h, w = mirrored.shape[:2]
    target_ratio = 9 / 16
    current_ratio = w / h if h else target_ratio
    crop_margin = 0.05  # slightly zoomed out feel

    if current_ratio > target_ratio:
        # Too wide → crop width
        new_w = int(h * target_ratio * (1 - crop_margin))
        x1 = max(0, (w - new_w) // 2)
        cropped = mirrored[:, x1:x1 + new_w]
        print(f"[VIEW] Cropped width: {w}->{new_w} (x1={x1})")
    else:
        # Too tall → crop height
        new_h = int(w / target_ratio * (1 - crop_margin))
        y1 = max(0, (h - new_h) // 2)
        cropped = mirrored[y1:y1 + new_h, :]
        print(f"[VIEW] Cropped height: {h}->{new_h} (y1={y1})")

    ch, cw = cropped.shape[:2]
    print(f"[VIEW] Output (cropped) frame: {cw}×{ch} (9:16 portrait)")
    return cropped

def prepare_for_yolo(frame: np.ndarray) -> Tuple[np.ndarray, bool]:
    """Prepare frame for YOLO input (no rotation needed)."""
    return frame, False

def letterbox_9_16(
    img: np.ndarray, target_w: int, target_h: int
) -> Tuple[np.ndarray, float, int, int]:
    """Resize + pad to 9:16 portrait without stretching."""
    h, w = img.shape[:2]
    scale = min(target_w / w, target_h / h)

    new_w = int(round(w * scale))
    new_h = int(round(h * scale))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    pad_left = (target_w - new_w) // 2
    pad_top = (target_h - new_h) // 2
    pad_right = target_w - new_w - pad_left
    pad_bottom = target_h - new_h - pad_top

    color = (114, 114, 114)
    padded = cv2.copyMakeBorder(
        resized, pad_top, pad_bottom, pad_left, pad_right,
        borderType=cv2.BORDER_CONSTANT, value=color
    )

    return padded, scale, pad_left, pad_top

def map_bbox_to_portrait(
    bbox: Tuple[float, float, float, float], transform: Dict
) -> Tuple[int, int, int, int]:
    """Map YOLO bbox back to portrait display coordinates."""
    x1, y1, x2, y2 = bbox
    yolo_scale = transform["yolo_scale"]
    yolo_pad_left = transform["yolo_pad_left"]
    yolo_pad_top = transform["yolo_pad_top"]
    cam_w = transform["cam_w"]
    cam_h = transform["cam_h"]

    x1_src = (x1 - yolo_pad_left) / yolo_scale
    y1_src = (y1 - yolo_pad_top) / yolo_scale
    x2_src = (x2 - yolo_pad_left) / yolo_scale
    y2_src = (y2 - yolo_pad_top) / yolo_scale

    disp_w = transform.get("rot_w", cam_w)
    disp_h = transform.get("rot_h", cam_h)
    mirrored = transform.get("mirrored", True)

    def clamp(v, lo, hi): return max(lo, min(hi, v))

    if mirrored:
        x1_i = clamp(int(round(disp_w - x1_src)), 0, disp_w)
        x2_i = clamp(int(round(disp_w - x2_src)), 0, disp_w)
    else:
        x1_i = clamp(int(round(x1_src)), 0, disp_w)
        x2_i = clamp(int(round(x2_src)), 0, disp_w)

    y1_i = clamp(int(round(y1_src)), 0, disp_h)
    y2_i = clamp(int(round(y2_src)), 0, disp_h)

    return min(x1_i, x2_i), min(y1_i, y2_i), max(x1_i, x2_i), max(y1_i, y2_i)

# =====================================================
# Drawing helpers
# =====================================================
BOX_COLOR = (0, 255, 0)
TEXT_BG_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX

def draw_detections(frame: np.ndarray, detections: list, transform: Dict):
    out = frame.copy()
    for det in detections:
        bbox = det.get("bbox", det)
        x1, y1, x2, y2 = map_bbox_to_portrait(bbox, transform)
        conf = det.get("confidence", 0.0)
        clsname = det.get("class_name", str(det.get("class_id", "obj")))

        cv2.rectangle(out, (x1, y1), (x2, y2), BOX_COLOR, 3)
        label = f"{clsname} {conf:.0%}"
        (label_w, label_h), _ = cv2.getTextSize(label, FONT, 0.7, 2)
        label_y = y1 - 10 if y1 - 10 > label_h else y1 + label_h + 10
        cv2.rectangle(out, (x1, label_y - label_h - 5),
                      (x1 + label_w + 10, label_y + 5), TEXT_BG_COLOR, -1)
        cv2.putText(out, label, (x1 + 5, label_y),
                    FONT, 0.7, TEXT_COLOR, 2, cv2.LINE_AA)
    return out

def draw_info(frame: np.ndarray, fps: float, count: int, processing: bool):
    out = frame.copy()
    h, w = frame.shape[:2]
    overlay = out.copy()
    cv2.rectangle(overlay, (10, 10), (w - 10, 180), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, out, 0.4, 0, out)
    info = [
        f"FPS: {fps:.1f}",
        f"Detections: {count}",
        f"View: PORTRAIT (upright)",
        f"Display: {w}×{h}",
        f"YOLO: {YOLO_WIDTH}×{YOLO_HEIGHT}",
    ]
    for i, text in enumerate(info):
        cv2.putText(out, text, (20, 45 + i * 25),
                    FONT, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    status = "Processing..." if processing else "Ready"
    color = (0, 255, 255) if processing else (0, 255, 0)
    cv2.putText(out, status, (20, 45 + len(info) * 25),
                FONT, 0.7, color, 2, cv2.LINE_AA)
    return out

# =====================================================
# Main loop
# =====================================================
def main():
    global processing, last_transform, current_detections, detection_count

    print("\n" + "=" * 60)
    print("Starting YOLOv11x Webcam Test (Portrait Mode)")
    print("=" * 60)
    print("\nMake sure the server is running in another window!")
    input("Press any key to continue...\n\n")

    print("[INFO] Connecting to server...")
    try:
        sio.connect(SERVER_URL)
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        return

    print("[INFO] Opening camera...")
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera")
        return

    cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[CAMERA] Resolution: {cam_w}×{cam_h}")

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(WINDOW_NAME, 720, 1280)
    print("[DISPLAY] Window: 720×1280 (Portrait 9:16)\n")

    print("=" * 60)
    print("[INFO] 📱 PORTRAIT VIEW MODE ACTIVE (upright)")
    print("[INFO] Press 'q' to quit, 'f' for fullscreen")
    print("=" * 60 + "\n")

    frame_count, fps, fullscreen = 0, 0.0, False
    start_time, last_send_time = time.time(), 0

    while True:
        ret, camera_frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame")
            break

        rotated_frame = rotate_to_portrait(camera_frame)
        yolo_frame, _ = prepare_for_yolo(rotated_frame)
        padded, scale, pad_left, pad_top = letterbox_9_16(
            yolo_frame, YOLO_WIDTH, YOLO_HEIGHT
        )

        last_transform = {
            "cam_w": cam_w,
            "cam_h": cam_h,
            "yolo_scale": scale,
            "yolo_pad_left": pad_left,
            "yolo_pad_top": pad_top,
            "rot_w": rotated_frame.shape[1],
            "rot_h": rotated_frame.shape[0],
            "mirrored": True,
        }

        now = time.time()
        if (now - last_send_time) >= FRAME_DELAY and not processing:
            processing = True
            try:
                b64 = encode_frame(padded, 80)
                sio.emit("frame", {"image": b64})
            except Exception as e:
                print(f"[ERROR] Send failed: {e}")
                processing = False
            last_send_time = now

        display = rotated_frame
        if last_transform and current_detections:
            display = draw_detections(display, current_detections, last_transform)

        frame_count += 1
        elapsed = time.time() - start_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count, start_time = 0, time.time()

        display = draw_info(display, fps, detection_count, processing)
        cv2.imshow(WINDOW_NAME, display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n[INFO] Quitting...")
            break
        elif key == ord("f"):
            fullscreen = not fullscreen
            mode = cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL
            cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, mode)
            print(f"[INFO] Fullscreen: {'ON' if fullscreen else 'OFF'}")

    print("[INFO] Cleaning up...")
    cap.release()
    cv2.destroyAllWindows()
    sio.disconnect()
    print("[INFO] Done.\n")


if __name__ == "__main__":
    main()
