import os
import json
import cv2
from paddleocr import PaddleOCR
import argparse

# Initialize PaddleOCR with English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# Set up command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="OCR Text Extraction from Images")
    parser.add_argument('--input_dir', type=str, required=True, help="Directory containing images to process")
    parser.add_argument('--output_image_dir', type=str, required=True, help="Directory to save annotated images")
    parser.add_argument('--output_json', type=str, required=True, help="Path to save JSON output with OCR results")
    return parser.parse_args()

# Main OCR processing function
def ocr_processing(input_dir, output_image_dir, output_json):
    # Ensure output directory exists
    os.makedirs(output_image_dir, exist_ok=True)

    # Initialize list to store OCR results
    ocr_results = []

    # Process each image in the input directory
    for image_name in os.listdir(input_dir):
        if image_name.lower().endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(input_dir, image_name)
            image = cv2.imread(image_path)

            # Run OCR on the image
            results = ocr.ocr(image_path, cls=True)

            if not results or not results[0]:  # Skip if no text detected
                print(f"❌ No text detected in {image_name}, skipping.")
                continue

            extracted_data = {"image_name": image_name, "texts": []}

            # Process and visualize results
            for res in results[0]:  # Iterate over detected text regions
                bbox, (text, confidence) = res
                if confidence > 0.80:  # Apply confidence threshold
                    print(f"✅ Detected text: {text} (Confidence: {confidence:.2f})")

                    # Extract bounding box coordinates
                    x_min, y_min = map(int, bbox[0])
                    x_max, y_max = map(int, bbox[2])

                    # Draw bounding boxes on the image
                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    cv2.putText(image, text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, (0, 255, 0), 1, cv2.LINE_AA)

                    # Save extracted text and bounding box
                    extracted_data["texts"].append({
                        "text": text,
                        "bbox": bbox,
                        "confidence": confidence
                    })

            # Save annotated image only if text was detected
            if extracted_data["texts"]:
                output_image_path = os.path.join(output_image_dir, image_name)
                cv2.imwrite(output_image_path, image)
                ocr_results.append(extracted_data)
            else:
                print(f"⚠️ No high-confidence text found in {image_name}, skipping.")

    # Save results in JSON format
    with open(output_json, "w") as f:
        json.dump(ocr_results, f, indent=4)

    print(f"\n🎯 OCR processing completed.")
    print(f"📄 JSON results saved: {output_json}")
    print(f"🖼 Annotated images saved in: {output_image_dir}")

# Run the OCR process with the command-line arguments
if __name__ == "__main__":
    args = parse_args()
    ocr_processing(args.input_dir, args.output_image_dir, args.output_json)
