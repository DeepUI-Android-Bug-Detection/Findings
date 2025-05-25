# YOLOv8 for UI Widget Detection

This section of the repository describes how to prepare, train, and use the YOLOv8 model for detecting UI elements in Android app screenshots. YOLO (You Only Look Once) is a real-time object detection system that will be used to identify UI components such as buttons, text fields, and other interactive elements.

## Overview

The process involves the following steps:
1. **Convert XML Annotations to YOLO Format**: Use `processing.py` to convert XML annotations (e.g., from LabelImg) to YOLO-friendly format.
2. **Train YOLO Model**: Use the converted data to train a YOLO model for detecting UI widgets in screenshots.
3. **Detect UI Widgets with the Trained YOLO Model**: Feed new screenshots into the trained YOLO model to detect UI components.

## Requirements

- Python 3.x
- YOLOv8 (Install from the official [Ultralytics repository](https://github.com/ultralytics/ultralytics))
- OpenCV
- NumPy
- LabelImg (for creating XML annotations, if you don't already have them)
- Other dependencies specified in `requirements.txt`

## Step 1: Convert XML Annotations to YOLO Format

The first step is to convert XML annotations (e.g., from LabelImg) into the YOLO format, which is needed for training. To do this, we use the `processing.py` script.

### Usage:

```bash
python processing.py --xml_dir <path_to_xml_annotations> --output_dir <path_to_yolo_format_output>
