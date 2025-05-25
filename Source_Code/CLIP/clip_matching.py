import json
import torch
import open_clip
import numpy as np
from PIL import Image
import faiss
from sklearn.preprocessing import normalize
import argparse

# Argument parser for CLI
parser = argparse.ArgumentParser(description="Match UI widgets with RICO captions using CLIP and FAISS.")
parser.add_argument("--yolo_results", type=str, required=True, help="Path to YOLO results JSON file.")
parser.add_argument("--rico_captions", type=str, required=True, help="Path to RICO widget captions JSON file.")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the matched results.")
args = parser.parse_args()

# Load the RICO Widget Captioning dataset
with open(args.rico_captions, "r") as f:
    rico_captions = json.load(f)

# Load CLIP Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = open_clip.create_model_and_transforms("ViT-B/32", pretrained="openai")
tokenizer = open_clip.get_tokenizer("ViT-B/32")

# Load YOLO results (bounding boxes and OCR text)
with open(args.yolo_results, "r") as f:
    yolo_results = json.load(f)

# Function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# FAISS Setup: Create index for fast caption retrieval
rico_texts = [rico["caption"] for rico in rico_captions]
rico_embeddings = []

# Create embeddings for RICO captions
for caption in rico_texts:
    text_tokenized = tokenizer([caption]).to(device)
    with torch.no_grad():
        text_embedding = model.encode_text(text_tokenized)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)  # Normalize embeddings
    rico_embeddings.append(text_embedding.cpu().numpy())

# Normalize the embeddings
rico_embeddings = np.vstack(rico_embeddings)
rico_embeddings = normalize(rico_embeddings, axis=1)


index = faiss.IndexFlatL2(rico_embeddings.shape[1])  # L2 distance (Euclidean)
index.add(rico_embeddings)  

# Function to process each widget
def process_widgets(yolo_results):
    ui_analysis = []
    for item in yolo_results:
        image_name = item["image_name"]
        img = Image.open(f"/path/to/images/{image_name}").convert("RGB")
        
        for widget in item["texts"]:
            bbox = widget["bbox"]
            text = widget["text"]
            confidence = widget["confidence"]

            # Crop the detected widget from the image
            x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
            x_max, y_max = int(bbox[2][0]), int(bbox[2][1])
            cropped_widget = img.crop((x_min, y_min, x_max, y_max))

            # Preprocess & encode with CLIP
            image_tensor = preprocess(cropped_widget).unsqueeze(0).to(device)
            with torch.no_grad():
                image_embedding = model.encode_image(image_tensor)
            image_embedding /= image_embedding.norm(dim=-1, keepdim=True)  # Normalize embeddings

            # Find the closest caption in the RICO dataset 
            D, I = index.search(image_embedding.cpu().numpy(), k=1)  # Search for top 1 match
            best_caption = rico_texts[I[0][0]]  # Get the best matched caption

            # Add widget description to UI analysis
            ui_analysis.append(f"- The screen contains a '{best_caption}' (Detected: {text}, Confidence: {confidence:.2f})")
    
    return ui_analysis

# Run the analysis
ui_analysis = process_widgets(yolo_results)

# Print Final UI Analysis
print("\n**UI Screenshot Analysis**")
for line in ui_analysis:
    print(line)

# Save the results to the output directory
output_file = f"{args.output_dir}/matched_results.json"
with open(output_file, "w") as f:
    json.dump(ui_analysis, f, indent=4)

print(f"\n Results saved to {output_file}")
