# Combining Multi-Modal UI Understanding with LLMs for Android Non-Crash Bug Detection

## Table of Contents
- [Overview](#Overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Evaluation](#evaluation)
- [Citation](#citation)


## Overview

![DeepUI Overview](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/overview.png?raw=true)

DeepUI is a novel approach for detecting non-crash bugs in Android applications by combining **multi-modal UI understanding** with **large language models** (LLMs) like GPT-4. This framework utilizes UI screenshots and user interactions to identify subtle bugs that are challenging for traditional bug detection tools.

DeepUI employs a two-stage pipeline to automatically and accurately detect non-crash bugs in Android apps:

1. **Multi-Modal UI Understanding:** 
   - Capture screenshots from the app's UI through test case execution.
   - Use advanced models like **YOLOv8** for widget detection, **PaddleOCR** for text extraction, and **CLIP** for contextual understanding of UI components.
   - Convert UI data into natural language descriptions.

2. **LLM-based Bug Detection:**
   - Construct context-rich prompts incorporating the UI state and user actions.
   - Feed these prompts to **GPT-4** for reasoning about app functionality and identifying potential bugs.
   - Generate human-readable explanations.

This approach leverages the power of multimodal analysis and LLMs to detect bugs that are difficult to identify with conventional tools.

## Features

- Detects **non-crash bugs** in Android applications.
- Uses **YOLOv8** for real-time widget detection in screenshots.
- **PaddleOCR** for robust optical character recognition (OCR) on text within UIs.
- Contextual understanding through the fine-tuned **CLIP model** for accurate UI element description.
- Uses **GPT-4** for reasoning about visual cues and user flows to predict potential bugs.

  ## Directory Structure

This section provides an overview of the repository structure, including datasets and the source code for the DeepUI Android Non-Crash Bug Detection framework. 
- **[Dataset](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Dataset)**: Contains the dataset used for training and evaluation.
- **[CLIP](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Source_Code/CLIP)**: Contains source code related to the CLIP model, including fine-tuning and inference scripts.
- **[OCR](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Source_Code/OCR)**: Contains the Optical Character Recognition code to extract text from UI screenshots.
- **[YOLO](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Source_Code/YOLO)**: Contains YOLO-based code for detecting UI elements in screenshots.
- **[Proximity_matching](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Source_Code/Proximity_matching)**: Contains code for matching OCR text to detected UI elements using proximity-based methods.

![Directories Structure Diagram](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/directories.PNG?raw=true)



  ## Folder Structure

```plaintext
deepui-project/
│
├── Dataset/                              # Dataset used for evaluation
│   ├── Videos.txt                        # List of videos and images for dataset creation
├── Source_Code/ # Main source code for the project
│ ├── CLIP/ # Fine-tune and inference scripts
│ │ ├── fine_tune_clip.py # Fine-tune CLIP model
│ │ ├── clip_matching.py # Matching widgets with RICO captions using CLIP
│ │ ├── clip_inference.py# Perform inference using fine-tuned CLIP
│ │ └── readme.md # Documentation for CLIP-based code
│ ├── OCR/ # OCR text extraction scripts
│ │ ├── ocr_script.py # OCR processing and widget matching
│ │ └── readme.md # Documentation for OCR code
│ ├── Proximity_matching/ # Proximity matching for OCR and widget bounding boxes
│ │ ├── proximity_matching.py # Match OCR text to detected widgets
│ │ └── readme.md # Documentation for proximity matching code
│ └── YOLO/ # YOLO object detection for UI widgets
│ ├── infer.py # Inference script for YOLO
│ ├── processing.py # YOLO annotation processing
│ └── readme.md # Documentation for YOLO code
├── overview.png # Diagram of the approach
├── README.md # This file
└── requirements.txt # Python dependencies


