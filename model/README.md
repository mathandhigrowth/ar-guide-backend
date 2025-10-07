# Model Directory

Place your trained YOLOv11x model weights here.

## Required File
- `best.pt` - Your trained YOLOv11x model weights

## Model Information
The server expects a YOLOv11x model file named `best.pt` in this directory.

### How to add your model:
1. Copy your trained model file to this directory
2. Rename it to `best.pt` or update the path in `server.py`
3. Restart the server

### Model Format
- Supported: PyTorch (.pt) format
- Recommended: YOLOv11x trained weights

### Example:
```bash
# Copy your model to this directory
cp /path/to/your/model.pt model/best.pt
```

## Notes
- Model files are ignored by git (too large)
- For deployment, ensure the model is included in your Docker image or mounted as a volume
- The model should be compatible with the installed ultralytics version

