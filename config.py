"""
Configuration file for YOLOv11x Backend Server
Adjust these settings to optimize detection accuracy and performance
"""

# ============================================================
# INFERENCE SETTINGS
# ============================================================

# Minimum confidence threshold (0.0 - 1.0)
# Higher = More accurate but fewer detections
# Lower = More detections but less accurate
CONFIDENCE_THRESHOLD = 0.01  # 1% confidence minimum (extremely low for testing)

# IoU threshold for Non-Maximum Suppression (0.0 - 1.0)
# Higher = More overlapping boxes allowed
# Lower = Fewer overlapping boxes
IOU_THRESHOLD = 0.45

# Image size for inference (larger = more accurate but slower)
# Common values: 320, 640, 1280
IMAGE_SIZE = 640

# Device for inference
# Options: 'cpu', 'cuda', 'cuda:0', 'cuda:1'
DEVICE = "cpu"

# Half precision (FP16) inference - Only for GPU
# Set to True for faster GPU inference
HALF_PRECISION = False

# ============================================================
# SERVER SETTINGS
# ============================================================

# Server host and port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 3000

# CORS allowed origins (for web clients)
CORS_ORIGINS = "*"  # Change to specific domains in production

# ============================================================
# MODEL SETTINGS
# ============================================================

# Path to model weights
MODEL_PATH = "model/yolo11s.pt"

# Enable/disable verbose inference output
VERBOSE_INFERENCE = False

# ============================================================
# OPTIMIZATION SETTINGS
# ============================================================

# Maximum detection limit per frame
MAX_DETECTIONS = 300

# Agnostic NMS (class-agnostic Non-Maximum Suppression)
AGNOSTIC_NMS = False

# Additional YOLO parameters
YOLO_PARAMS = {
    "conf": CONFIDENCE_THRESHOLD,
    "iou": IOU_THRESHOLD,
    "verbose": VERBOSE_INFERENCE,
    "device": DEVICE,
    "half": HALF_PRECISION,
    "max_det": MAX_DETECTIONS,
    "agnostic_nms": AGNOSTIC_NMS,
}

# ============================================================
# QUALITY PRESETS
# ============================================================

# Uncomment one of these presets or use custom settings above

# PRESET 1: High Accuracy (Slower, 70%+ confidence)
PRESET_HIGH_ACCURACY = {
    "conf": 0.5,
    "iou": 0.45,
    "max_det": 100,
}

# PRESET 2: Balanced (Medium speed and accuracy, 60%+ confidence)
PRESET_BALANCED = {
    "conf": 0.6,
    "iou": 0.5,
    "max_det": 200,
}

# PRESET 3: High Recall (Faster, more detections, 40%+ confidence)
PRESET_HIGH_RECALL = {
    "conf": 0.4,
    "iou": 0.5,
    "max_det": 300,
}

# PRESET 4: Very High Accuracy (Strictest, 80%+ confidence)
PRESET_VERY_HIGH_ACCURACY = {
    "conf": 0.8,
    "iou": 0.4,
    "max_det": 50,
}

# Select active preset (or set to None to use YOLO_PARAMS)
ACTIVE_PRESET = "HIGH_RECALL"  # Options: 'HIGH_ACCURACY', 'BALANCED', 'HIGH_RECALL', 'VERY_HIGH_ACCURACY', None (using HIGH_RECALL for Flutter debugging)

# Apply preset if selected
if ACTIVE_PRESET == "HIGH_ACCURACY":
    YOLO_PARAMS.update(PRESET_HIGH_ACCURACY)
elif ACTIVE_PRESET == "BALANCED":
    YOLO_PARAMS.update(PRESET_BALANCED)
elif ACTIVE_PRESET == "HIGH_RECALL":
    YOLO_PARAMS.update(PRESET_HIGH_RECALL)
elif ACTIVE_PRESET == "VERY_HIGH_ACCURACY":
    YOLO_PARAMS.update(PRESET_VERY_HIGH_ACCURACY)

# ============================================================
# DISPLAY SETTINGS (for test client)
# ============================================================

# Show confidence percentage on bounding boxes
SHOW_CONFIDENCE = True

# Show class IDs
SHOW_CLASS_ID = False

# Bounding box color (B, G, R)
BBOX_COLOR = (0, 255, 0)  # Green

# Bounding box thickness
BBOX_THICKNESS = 2

# Font scale for labels
FONT_SCALE = 0.5

# ============================================================
# FRAME PROCESSING SETTINGS
# ============================================================

# Maximum frame dimension for preprocessing (reduces bandwidth)
# Larger values = better quality but more bandwidth
# Smaller values = faster processing but lower quality
FRAME_MAX_DIM = 640  # Resize frames to max 640px on longest side

# ============================================================
# PERFORMANCE TIPS
# ============================================================

"""
For Better Accuracy:
- Increase CONFIDENCE_THRESHOLD (0.7 - 0.9)
- Decrease IOU_THRESHOLD (0.3 - 0.45)
- Increase IMAGE_SIZE (640 - 1280)
- Use HIGH_ACCURACY or VERY_HIGH_ACCURACY preset

For Better Performance (Speed):
- Decrease CONFIDENCE_THRESHOLD (0.3 - 0.5)
- Use smaller IMAGE_SIZE (320 - 640)
- Enable HALF_PRECISION (GPU only)
- Use BALANCED or HIGH_RECALL preset

For GPU Acceleration:
- Set DEVICE = 'cuda'
- Set HALF_PRECISION = True
- Restart server

Current Settings:
- Confidence: {conf:.0%}
- IoU: {iou}
- Device: {device}
- Preset: {preset}
""".format(
    conf=YOLO_PARAMS["conf"],
    iou=YOLO_PARAMS["iou"],
    device=DEVICE,
    preset=ACTIVE_PRESET or "Custom",
)
