# Combining Multi-Modal UI Understanding with LLMs for Android Non-Crash Bug Detection

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Dataset for Android Non-Crash Bug Detection](#dataset-for-android-non-crash-bug-detection)
- [Download Dataset](#download-dataset)
- [Usage Instructions](#usage-instructions)
- [Installation](#installation)
- [Folder Structure](#folder-structure)


## Overview

![DeepUI Overview](https://github.com/DeepUI-Android-Bug-Detection/Findings/blob/main/Overview.PNG?raw=true)
DeepUI is a novel approach for detecting non-crash bugs in Android applications by combining **multi-modal UI understanding** with **large language models** (LLMs) like GPT-4. This framework utilizes UI screenshots and user interactions to identify subtle bugs that are challenging for traditional bug detection tools.

DeepUI employs a two-stage pipeline to automatically and accurately detect non-crash bugs in Android apps:

1. **Multi-Modal UI Understanding:** 
   - Capture screenshots from the app's UI through test case execution.
   - Use advanced models like **YOLOv8** for widget detection, **PaddleOCR** for text extraction, and **CLIP** for contextual understanding of UI components.
   - Convert UI data into natural language descriptions.
  
2. **GPT-4 Detection**
   - Feed the generated textual representation into GPT-4.

This repository contains the code, datasets, and resources for the research paper "Combining Multi-Modal UI Understanding with LLMs for Android Non-Crash Bug Detection". The proposed method is used to detect on-crash bugs in Android applications. 

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



  ## Dataset for Android Non-Crash Bug Detection

This folder contains all the datasets used for evaluation of the approach in the paper "Combining Multi-Modal UI Understanding with LLMs for Android Non-Crash Bug Detection." The dataset is organized into two main parts: Videos dataset containing the reproduction videos and GUI images dataset.


This dataset is used to evaluate the DeepUI system. It includes real-world Android app bug reproduction scenarios.

Videos Dataset
Contains screen-recorded videos of actual app usage where non-crash bugs occur.

These videos are used to extract frames for widget detection and UI analysis.

Images Dataset
Contains annotated UI screenshots extracted from the videos.

Screenshots are used by YOLOv8, PaddleOCR, and CLIP for multi-modal analysis.





Main directory containing dataset of reproduction videos and images.
```plaintext
Dataset/
├── 📁 Videos Dataset # Contains video files of the bug reproduction. 
│ ├── app.webm/ 
├── 📁Images Dataset #Contains image files of the bug reproduction.
 ├── bug.png


```

## Download Dataset
Due to size limits, the dataset has been uploaded to Google Drive. You can download the dataset using the following link:

[Download Videos Dataset](https://drive.google.com/drive/folders/1247QANbLqh0VrlEofxTjlBrKeeAQEDXU?usp=sharing)
[Download Images Dataset](https://drive.google.com/drive/folders/10clpqxQglLLjwcLrNwlk0Cz5_RpDYHcU?usp=sharing)


##  Usage Instructions

This guide describes how to use the Images Dataset in the DeepUI pipeline for detecting non-crash bugs in Android apps.

##  Steps

1. **Widget Detection with YOLOv8**
   - Use the `Images Dataset` as input to the YOLOv8 model.
   - YOLOv8 will detect UI widgets such as buttons, input fields, sliders, etc.

2. **Text Extraction with PaddleOCR**
   - Run PaddleOCR on the same images to extract visible text from UI components.
   - Captures labels, tooltips, error messages, and other textual information.
     
3. **Proximity Matching**
   - Matches OCR text to widgets based on spatial layout

4. **Contextual Understanding with CLIP**
   - Combine the outputs of YOLO (bounding boxes) and OCR (text) and pass them into the CLIP model.
   - CLIP generates contextual embeddings that associate UI elements with their textual labels and layout.

5. **Bug Detection with GPT-4**
   - Feed the generated textual representation into GPT-4.
   - GPT-4 performs reasoning on the interface to detect logical and UI-related bugs (non-crash issues).

## Dataset Role

These datasets are an integral part of the **DeepUI** pipeline, which fuses **vision**, **text**, and **reasoning** to support **non-crash bug detection** in Android applications.


## Installation

Follow these steps to set up the environment for running the **DeepUI** pipeline.

## 1. Clone the Repository
```bash
git clone https://github.com/DeepUI-Android-Bug-Detection/DeepUI.git
cd DeepUI
```
## 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 2. Install the Required Packages
```bash

pip install -r requirements.txt
```
  ## Folder Structure

```plaintext
Dataset/
├── 📁 Videos Dataset # Contains video files of the bug reproduction. 
│ ├── app.webm/ 
├── 📁Images Dataset #Contains image files of the bug reproduction.
 ├── bug.png                      # List of videos and images for dataset creation
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
```

