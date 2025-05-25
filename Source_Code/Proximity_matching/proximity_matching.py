import os
import json
import numpy as np
import argparse

# Set up command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Proximity Matching of OCR Text and YOLO Widgets")
    parser.add_argument('--yolo_labels_dir', type=str, required=True, help="Directory containing YOLO label files")
    parser.add_argument('--ocr_json_path', type=str, required=True, help="Path to the OCR JSON file")
    parser.add_argument('--output_json_path', type=str, required=True, help="Path to save the proximity-matched results JSON file")
    return parser.parse_args()

# Function to calculate the Euclidean distance between two bounding boxes
def calculate_distance(box1, box2):
    center1 = ((box1[0] + box1[2]) / 2, (box1[1] + box1[3]) / 2)
    center2 = ((box2[0] + box2[2]) / 2, (box2[1] + box2[3]) / 2)
    return np.linalg.norm(np.array(center1) - np.array(center2))

# Function to parse YOLO labels
def parse_yolo_labels(label_path, img_width, img_height):
    yolo_boxes = []
    with open(label_path, "r") as f:
        for line in f:
            data = line.strip().split()
            class_id = int(data[0])
            x_center, y_center, width, height = map(float, data[1:])
            
            # Convert YOLO format to absolute pixel coordinates
            x_min = int((x_center - width / 2) * img_width)
            y_min = int((y_center - height / 2) * img_height)
            x_max = int((x_center + width / 2) * img_width)
            y_max = int((y_center + height / 2) * img_height)

            yolo_boxes.append({"class_id": class_id, "bbox": [x_min, y_min, x_max, y_max]})
    return yolo_boxes

# Main function for proximity matching
def proximity_matching(yolo_labels_dir, ocr_json_path, output_json_path):
    # Load OCR results
    with open(ocr_json_path, "r") as f:
        ocr_data = json.load(f)

    proximity_results = []
    
    # Process each OCR entry
    for ocr_entry in ocr_data:
        image_name = ocr_entry["image_name"]
        label_file = os.path.join(yolo_labels_dir, image_name.replace(".jpg", ".txt"))

        if not os.path.exists(label_file):
            print(f"Skipping {image_name}, no YOLO label found.")
            continue

        # Assuming all images have the same resolution (modify if needed)
        IMAGE_WIDTH, IMAGE_HEIGHT = 1080, 1920  # Adjust if different

        yolo_boxes = parse_yolo_labels(label_file, IMAGE_WIDTH, IMAGE_HEIGHT)
        matched_entries = {"image_name": image_name, "ui_elements": []}

        # Match OCR text to the nearest YOLO bounding box
        for yolo_box in yolo_boxes:
            closest_text = None
            min_distance = float("inf")

            for text_entry in ocr_entry["texts"]:
                ocr_bbox = [
                    int(text_entry["bbox"][0][0]), int(text_entry["bbox"][0][1]),
                    int(text_entry["bbox"][2][0]), int(text_entry["bbox"][2][1])
                ]

                distance = calculate_distance(yolo_box["bbox"], ocr_bbox)
                if distance < min_distance:
                    min_distance = distance
                    closest_text = text_entry["text"]

            matched_entries["ui_elements"].append({
                "class_id": yolo_box["class_id"],
                "bbox": yolo_box["bbox"],
                "matched_text": closest_text if closest_text else "No text nearby"
            })

        proximity_results.append(matched_entries)

    # Save results
    with open(output_json_path, "w") as f:
        json.dump(proximity_results, f, indent=4)

    print(f" Proximity matching completed!")
    print(f" JSON results saved: {output_json_path}")

# Run the proximity matching process
if __name__ == "__main__":
    args = parse_args()
    proximity_matching(args.yolo_labels_dir, args.ocr_json_path, args.output_json_path)
