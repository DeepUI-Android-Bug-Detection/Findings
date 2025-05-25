# Proximity Matching

This repository contains a script for matching **OCR-extracted text** with **YOLO-detected UI elements** in images. It uses proximity-based matching, where the OCR text is associated with the closest widget (bounding box) detected by YOLO.

The script first reads YOLO label files for detected widgets and OCR results for detected text. Then, it calculates the proximity (distance) between OCR text and widget bounding boxes to match text with widgets. Finally, it saves the matched results in a JSON file.


## Features

- **Proximity-Based Matching**: Matches OCR text with the closest detected widget based on the Euclidean distance between bounding boxes.
- **Text and Widget Association**: Associates the OCR text with YOLO-detected widgets, including class labels and bounding boxes.
- **JSON Output**: Saves the matched results as a JSON file containing the widget information along with associated OCR text.


## Requirements

- Python 3.x
- numpy
- OpenCV
- json

## Usage

### Step 1: Set Up Your Input and Output Directories

Before running the script, you need to specify the following directories:

- **YOLO Labels Directory**: Directory containing YOLO label files (`*.txt` files with bounding box information for widgets).
- **OCR JSON Path**: Path to the OCR results JSON file containing extracted text and bounding boxes.
- **Output JSON Path**: Path where the proximity-matched results will be saved as a JSON file.

### Step 2: Run the Script

To execute the script, run the following command:

```bash
python proximity_matching.py --yolo_labels_dir <path_to_yolo_labels> --ocr_json_path <path_to_ocr_json> --output_json_path <path_to_output_json>

