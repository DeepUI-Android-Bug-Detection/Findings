import torch
from transformers import CLIPProcessor, CLIPModel
import json
import os
from pathlib import Path
from PIL import Image
import argparse

# Argument parser for CLI
parser = argparse.ArgumentParser(description="Perform inference with the fine-tuned CLIP model to match UI screenshots with descriptions.")
parser.add_argument("--image_dir", type=str, required=True, help="Path to the directory containing UI screenshots.")
parser.add_argument("--ui_descriptions", type=str, required=True, help="Path to the UI descriptions JSON file.")
parser.add_argument("--model_path", type=str, required=True, help="Path to the fine-tuned CLIP model.")
parser.add_argument("--output_json", type=str, required=True, help="Path to save the output results.")
args = parser.parse_args()

# Load fine-tuned CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained(args.model_path).to(device)
processor = CLIPProcessor.from_pretrained(args.model_path)

# Load UI descriptions
with open(args.ui_descriptions, "r") as f:
    ui_descriptions = json.load(f)

# Normalize JSON keys (lowercase) for better matching
ui_descriptions = {k.lower().strip(): v for k, v in ui_descriptions.items()}

# Debug JSON keys
print("📌 First 10 JSON keys:", list(ui_descriptions.keys())[:10])

# Truncate descriptions to avoid CLIP token limit
def truncate_text(text, max_tokens=512):
    tokens = text.split()
    return " ".join(tokens[:max_tokens])

# Prepare text embeddings
text_descriptions = [truncate_text(desc) for desc in ui_descriptions.values()]
text_inputs = processor(text=text_descriptions, padding=True, truncation=True, return_tensors="pt").to(device)

with torch.no_grad():
    text_embeddings = model.get_text_features(**text_inputs)
    text_embeddings /= text_embeddings.norm(dim=-1, keepdim=True)  # Normalize

# Dictionary to store results
results = {}

# Process images
for root, _, files in os.walk(args.image_dir):
    print("📌 First 10 image filenames:", files[:10])  # Debug filenames

    for file in files:
        if file.endswith(".png") and not file.startswith("._"):
            image_path = Path(root) / file

            # Handle mismatched extensions
            image_key_jpg = file.replace(".png", ".jpg").lower()
            image_key_png = file.lower()

            if image_key_jpg in ui_descriptions:
                image_key = image_key_jpg
            elif image_key_png in ui_descriptions:
                image_key = image_key_png
            else:
                print(f"⚠️ No description found for {file} (Looking for: {image_key_jpg} or {image_key_png})")
                continue  # Skip this image

            description = truncate_text(ui_descriptions[image_key])

            try:
                # Process image
                image = Image.open(image_path).convert("RGB")
                image_inputs = processor(images=image, return_tensors="pt").to(device)

                with torch.no_grad():
                    image_embedding = model.get_image_features(**image_inputs)
                    image_embedding /= image_embedding.norm(dim=-1, keepdim=True)  # Normalize

                    # Compute similarity
                    similarity = (image_embedding @ text_embeddings.T).squeeze(0)
                    best_match_idx = similarity.argmax().item()
                    best_match_score = similarity[best_match_idx].item()
                    best_match_text = text_descriptions[best_match_idx]

                # Print results
                print(f"📸 Processed: {image_path}")
                print(f"🔍 Best Matched UI Description (Score: {best_match_score:.2f}):\n{best_match_text}\n")

                # Store results
                results[file] = {
                    "best_match_description": best_match_text,
                    "similarity_score": round(best_match_score, 2)
                }

            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

# Save results to JSON
with open(args.output_json, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ Processing complete. Results saved to: {args.output_json}")
