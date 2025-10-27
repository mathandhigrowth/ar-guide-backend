# Model Directory

This directory contains the trained YOLOv11n model weights.

## Setup Instructions

1. Download your trained YOLOv11n model weights (best.pt file)
2. Place the `best.pt` file in this directory
3. The server will automatically load the model from `model/best.pt`

## Model Requirements

- Format: PyTorch (.pt) file
- Architecture: YOLOv11n (nano version for faster inference)
- Input size: 640x640 pixels (default)
- Classes: Depends on your training dataset

## Notes

- The model will be loaded automatically when the server starts
- Make sure the model file is named `best.pt` exactly
- For GPU acceleration, ensure CUDA is available and PyTorch is installed with CUDA support
