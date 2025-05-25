# OCR Text Extraction from Images

This repository contains a script that extracts text from images using **PaddleOCR**. The script processes images by detecting text regions and their corresponding bounding boxes, annotating the images with detected text, and saving the results (both images and extracted text) in JSON format.

This method is useful for extracting text from UI components detected by YOLO or other sources, making it ideal for processing Android screenshots or any image with textual content.


## Features

- **OCR Text Extraction**: Extracts text from images using **PaddleOCR**.
- **Bounding Box Visualization**: Draws bounding boxes around detected text and places the text on the image.
- **Confidence Threshold**: Filters results based on a confidence threshold.
- **Results Saving**: Saves annotated images and results in JSON format.


## Requirements

- Python 3.x
- PaddleOCR (Install from the official [PaddleOCR repository](https://github.com/PaddlePaddle/PaddleOCR))
- OpenCV


## Usage

### Step 1: Set Up Your Input and Output Directories

The script processes images found in the YOLO-predicted images folder and outputs results in two locations:

- **Annotated images** with bounding boxes drawn around detected text will be saved in `outputs/`.
- **Extracted text data** will be saved in a JSON file (`extracted_ui_text.json`).

You need to specify the input and output directories when running the script using command-line arguments.

### Step 2: Run the OCR Script

To execute the script, run the following command:

```bash
python ocr_script.py --input_dir <path_to_images> --output_image_dir <path_to_output_images> --output_json <path_to_output_json>
```
