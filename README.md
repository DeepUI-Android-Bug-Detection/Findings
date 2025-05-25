# Combining Multi-Modal UI Understanding with LLMs for Android Non-Crash Bug Detection

DeepUI is a novel approach for detecting non-crash bugs in Android applications by combining **multi-modal UI understanding** with **large language models** (LLMs) like GPT-4. This framework utilizes UI screenshots and user interactions to identify subtle bugs that are challenging for traditional bug detection tools.

## Overview

DeepUI employs a two-stage pipeline to automatically and accurately detect non-crash bugs in Android apps:

1. **Multi-Modal UI Understanding:** 
   - Capture screenshots from the app's UI through test case execution.
   - Use advanced models like **YOLOv8** for widget detection, **PaddleOCR** for text extraction, and **CLIP** for contextual understanding of UI components.
   - Convert UI data into natural language descriptions.

2. **LLM-based Bug Detection:**
   - Construct context-rich prompts incorporating the UI state and user actions.
   - Feed these prompts to **GPT-4** for reasoning about app functionality and identifying potential bugs.
   - Generate human-readable explanations and bug reports.

This approach leverages the power of multimodal analysis and LLMs to detect bugs that are difficult to identify with conventional tools.

## Features

- Detects **non-crash bugs** in Android applications without requiring source code or instrumentation.
- Uses **YOLOv8** for real-time widget detection in screenshots.
- **PaddleOCR** for robust optical character recognition (OCR) on text within UIs.
- Contextual understanding through the fine-tuned **CLIP model** for accurate UI element description.
- Uses **GPT-4** for reasoning about visual cues and user flows to predict potential bugs.
- **Human-readable bug reports** with detailed explanations of detected issues.

## Dataset

We have curated a benchmark dataset of 150 Android UI scenarios (75 buggy, 75 non-buggy), reproduced from real-world GitHub issues. The dataset includes:

- Video recordings of test case executions
- GUI screenshots extracted from these videos
- Detailed bug descriptions and reproduction steps

You can download the dataset here: [DeepUI Benchmark Dataset](https://drive.google.com/drive/folders/1247QANbLqh0VrlEofxTjlBrKeeAQEDXU?usp=drive_link)

## Installation

To install DeepUI and run it on your local machine, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/deepui.git
   cd deepui
