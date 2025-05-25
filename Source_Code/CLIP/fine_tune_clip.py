import torch
from transformers import CLIPProcessor, CLIPModel
import json
from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import argparse

# Argument parser for CLI
parser = argparse.ArgumentParser(description="Fine-tune CLIP model on RICO Widget Captioning dataset.")
parser.add_argument("--train_data", type=str, required=True, help="Path to RICO dataset (images and captions).")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the fine-tuned CLIP model.")
parser.add_argument("--batch_size", type=int, default=4, help="Batch size for training.")
parser.add_argument("--epochs", type=int, default=3, help="Number of epochs for training.")
args = parser.parse_args()

# Define Dataset Class
class RICODataset(Dataset):
    def __init__(self, data_path):
        with open(data_path, "r") as f:
            self.data = json.load(f)
        self.image_dir = Path(data_path).parent / "images"  # Assumes images are in 'images' subdirectory
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        image_path = self.image_dir / item["image_name"]
        image = Image.open(image_path).convert("RGB")
        caption = item["caption"]
        inputs = self.processor(text=[caption], images=image, return_tensors="pt", padding=True)
        return inputs

# Load the Dataset
dataset = RICODataset(args.train_data)
dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

# Load Pre-trained CLIP Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

# Set the optimizer and loss function
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

# Fine-tuning Loop
for epoch in range(args.epochs):
    model.train()
    total_loss = 0

    for batch in dataloader:
        input_ids = batch['input_ids'].squeeze(1).to(device)
        pixel_values = batch['pixel_values'].to(device)
        
        # Forward pass
        outputs = model(input_ids=input_ids, pixel_values=pixel_values, return_loss=True)
        loss = outputs.loss
        total_loss += loss.item()

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{args.epochs}, Loss: {avg_loss:.4f}")

# Save the fine-tuned model
model.save_pretrained(args.output_dir)
print(f"Fine-tuned model saved at {args.output_dir}")
