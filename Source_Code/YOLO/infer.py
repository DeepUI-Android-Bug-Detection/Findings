from ultralytics import YOLO
from pathlib import Path
import cv2
import json
import os
import argparse

def run_inference(weights_path, image_dir, output_dir):
    # Load the trained YOLO model
    model = YOLO(weights_path)

    # Directories for saving outputs
    output_img_dir = output_dir / 'annotated_images'
    output_label_dir = output_dir / 'labels'
    output_img_dir.mkdir(parents=True, exist_ok=True)
    output_label_dir.mkdir(parents=True, exist_ok=True)

    # Supported image extensions
    image_extensions = ['.png', '.jpg', '.jpeg']

    # Final result list for JSON
    all_results = []

    # Walk through all image files recursively
    for image_path in Path(image_dir).rglob('*'):
        if image_path.suffix.lower() in image_extensions and not image_path.name.startswith("._"):
            img = cv2.imread(str(image_path))
            if img is None:
                print(f" Skipping unreadable image: {image_path}")
                continue

            print(f" Running YOLO on: {image_path}")
            results = model(str(image_path))
            r = results[0]

            # Save annotated image
            out_img_path = output_img_dir / f"{image_path.stem}_pred.jpg"
            r.save(filename=str(out_img_path))

            # Prepare label and JSON data
            labels = []
            for box in r.boxes:
                cls_id = int(box.cls.item())
                conf = float(box.conf.item())
                xyxy = box.xyxy[0].tolist()
                x1, y1, x2, y2 = xyxy

                # Convert to YOLO format: (class, x_center, y_center, width, height) normalized
                img_h, img_w = img.shape[:2]
                x_center = (x1 + x2) / 2 / img_w
                y_center = (y1 + y2) / 2 / img_h
                width = (x2 - x1) / img_w
                height = (y2 - y1) / img_h

                label_line = f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                labels.append(label_line)

                all_results.append({
                    "image": str(image_path),
                    "class_id": cls_id,
                    "confidence": round(conf, 4),
                    "bbox_xyxy": [round(x, 2) for x in xyxy]
                })

            # Save YOLO .txt label file
            label_file_path = output_label_dir / f"{image_path.stem}.txt"
            with open(label_file_path, 'w') as f:
                f.write('\n'.join(labels))

    # Save all results to JSON
    json_path = output_dir / 'detections.json'
    with open(json_path, 'w') as jf:
        json.dump(all_results, jf, indent=2)

    print(f"\n Done! Outputs saved to: {output_dir}")
    print(f"- Annotated images: {output_img_dir}")
    print(f"- YOLO labels: {output_label_dir}")
    print(f"- JSON file: {json_path}")


if __name__ == "__main__":
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Run YOLO inference on images and save results")
    parser.add_argument('--weights', type=str, required=True, help="Path to the trained YOLO model weights file")
    parser.add_argument('--image_dir', type=str, required=True, help="Directory containing images to process")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the output (annotated images, labels, and JSON)")

    args = parser.parse_args()

    # Run the inference with provided arguments
    run_inference(args.weights, args.image_dir, Path(args.output_dir))
