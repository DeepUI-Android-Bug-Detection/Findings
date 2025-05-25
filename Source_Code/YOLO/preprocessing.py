import os
import xml.etree.ElementTree as ET
import cv2
import torch
import argparse

# Check for GPU availability
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

# Updated class mapping with 'TextButton'
class_map = {
    "BackgroundImage": 0, "CheckedTextView": 1, "Icon": 2, "EditText": 3, "Image": 4,
    "Text": 5, "Text Button": 6, "Drawer": 7, "PageIndicator": 8, "UpperTaskBar": 9,
    "Modal": 10, "Switch": 11, "Spinner": 12, "Card": 13, "Multi-tab": 14, "Toolbar": 15,
    "Bottom-Navigation": 16, "Remember": 17, "TextButton": 18  # Added TextButton to class_map
}

# Function to parse XML and extract bounding boxes
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    labels, bboxes = [], []
    
    for obj in root.findall("object"):
        label = obj.find("name").text
        if label not in class_map:
            print(f"Warning: Class '{label}' not in class_map. Skipping...")
            continue

        try:
            xmin = float(obj.find("bndbox/xmin").text)
            ymin = float(obj.find("bndbox/ymin").text)
            xmax = float(obj.find("bndbox/xmax").text)
            ymax = float(obj.find("bndbox/ymax").text)
        except ValueError as e:
            print(f"Error parsing bounding box coordinates for {label}: {e}")
            continue

        labels.append(label)
        bboxes.append([xmin, ymin, xmax, ymax])
    
    return labels, bboxes

# Convert bounding boxes to YOLO format
def convert_to_yolo_format(bounds, img_width, img_height):
    x_min, y_min, x_max, y_max = bounds
    x_center = (x_min + x_max) / (2 * img_width)
    y_center = (y_min + y_max) / (2 * img_height)
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height

# Main function to process the files
def process_files(xml_dir, image_dir, output_label_dir):
    os.makedirs(output_label_dir, exist_ok=True)

    # Process each XML file
    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, file)
            image_name = file.replace(".xml", ".jpg")
            image_path = os.path.join(image_dir, image_name)

            if not os.path.exists(image_path):
                print(f"Warning: Image {image_name} not found. Skipping {file}...")
                continue

            # Load image to get dimensions
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: Unable to read {image_name}. Skipping...")
                continue
            img_height, img_width, _ = img.shape

            # Parse XML
            labels, bboxes = parse_xml(xml_path)
            if not labels:
                print(f"Warning: No valid objects found in {file}. Skipping...")
                continue

            # Create YOLO annotation file
            label_file_path = os.path.join(output_label_dir, file.replace(".xml", ".txt"))
            with open(label_file_path, "w") as label_f:
                for i, bbox in enumerate(bboxes):
                    class_id = class_map[labels[i]]
                    x_center, y_center, width, height = convert_to_yolo_format(bbox, img_width, img_height)
                    label_f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

            print(f"Processed {file} -> {label_file_path}")

    print("All XML files processed successfully on", device)

# Command-line arguments setup
def main():
    parser = argparse.ArgumentParser(description="Convert XML annotations to YOLO format.")
    parser.add_argument("xml_dir", type=str, help="Directory containing the XML annotation files.")
    parser.add_argument("image_dir", type=str, help="Directory containing the image files.")
    parser.add_argument("output_label_dir", type=str, help="Directory to store YOLO label files.")

    args = parser.parse_args()

    # Process files with the provided directories
    process_files(args.xml_dir, args.image_dir, args.output_label_dir)

if __name__ == "__main__":
    main()
