# Semantic Descriptions with CLIP

This repository contains scripts for matching **UI widgets** in screenshots to their **semantic descriptions** using **CLIP** (Contrastive Language–Image Pretraining). The model has been fine-tuned on the **RICO Widget Captioning Dataset** to enhance its ability to understand and associate visual widgets with functional descriptions.



## Scripts

### `fine_tune_clip_model.py`

This script fine-tunes the **CLIP model** on the **RICO Widget Captioning Dataset**. It updates the model's parameters to better understand and match visual widgets with their functional descriptions.



### `clip_matching.py`

This script performs the **semantic matching** between detected UI widgets and **RICO widget captions** using the **CLIP model**. It processes YOLO detection results (bounding boxes and OCR text) and associates each widget with the most relevant description from the RICO dataset.

### `clip_inference.py`

This script performs **inference** with the fine-tuned **CLIP model** to compare **UI screenshots** to their corresponding **UI descriptions**. It outputs the **similarity score** between the image and the description.


## Requirements

- Python 3.x
- PyTorch
- Hugging Face Transformers
- open_clip
- scikit-learn
- Pillow



## Usage

### Step 1: Set Up Your Input and Output Directories

Before running the scripts, specify the following directories:

- **YOLO Results Directory**: Directory containing YOLO label files (bounding box and OCR results).
- **RICO Captions File**: JSON file with the RICO widget captions.
- **UI Descriptions File**: JSON file with UI descriptions for inference.
- **Fine-Tuned CLIP Model Directory**: Directory containing the fine-tuned CLIP model.
- **Output Directory**: Directory to save the output (e.g., matched results in JSON format).

### Step 2: Fine-Tune the CLIP Model

To fine-tune the CLIP model on the **RICO Widget Captioning Dataset**, use the following command:

```bash
python fine_tune_clip_model.py --train_data <path_to_rico_dataset> --output_dir <path_to_save_finetuned_model>
```
### Step 3: Run the Scripts

 To run the scripts use:

```bash
python clip_matching.py --yolo_results <path_to_yolo_results> --rico_captions <path_to_rico_captions> --output_dir <path_to_output_directory>
```


