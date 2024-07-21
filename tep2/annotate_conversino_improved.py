import os
import json
import cv2

# Paths to your dataset
labels_dir = "F:/LANE-DETECTION/DATASETS/LLAMAS/labels/labels"
images_dir = "F:/LANE-DETECTION/DATASETS/LLAMAS/grayscale_images"

# Function to convert to YOLO format
def convert_to_yolo_format(image_width, image_height, box):
    x_center = (box[0] + box[2]) / 2.0 / image_width
    y_center = (box[1] + box[3]) / 2.0 / image_height
    width = (box[2] - box[0]) / image_width
    height = (box[3] - box[1]) / image_height
    return x_center, y_center, width, height

# Loop through all JSON files
for root, dirs, files in os.walk(labels_dir):
    for label_file in files:
        if label_file.endswith(".json"):
            with open(os.path.join(root, label_file), 'r') as f:
                data = json.load(f)

            # Corresponding image path
            image_dir = os.path.join(images_dir, os.path.relpath(root, labels_dir).replace('labels', ''))
            image_file = label_file.replace('.json', '_gray_rect.png')
            image_path = os.path.join(image_dir, image_file)
            image = cv2.imread(image_path)
            image_height, image_width = image.shape[:2]

            # Output label file in YOLO format
            output_label_dir = os.path.join(os.path.dirname(root), 'YoloFormat', os.path.basename(root))
            os.makedirs(output_label_dir, exist_ok=True)
            yolo_label_file = os.path.join(output_label_dir, label_file.replace('.json', '.txt'))

            with open(yolo_label_file, 'w') as out_file:
                lanes = data.get('lanes', [])
                for lane in lanes:
                    markers = lane.get('markers', [])
                    for marker in markers:
                        pixel_start = marker.get('pixel_start', {})
                        pixel_end = marker.get('pixel_end', {})

                        # Extract coordinates and convert to integers
                        x_start = int(pixel_start.get('x', 0))
                        y_start = int(pixel_start.get('y', 0))
                        x_end = int(pixel_end.get('x', 0))
                        y_end = int(pixel_end.get('y', 0))

                        # Calculate bounding box
                        x_min = min(x_start, x_end)
                        y_min = min(y_start, y_end)
                        x_max = max(x_start, x_end)
                        y_max = max(y_start, y_end)

                        box = [x_min, y_min, x_max, y_max]
                        x_center, y_center, width, height = convert_to_yolo_format(image_width, image_height, box)

                        # Write to YOLO format
                        out_file.write(f"0 {x_center} {y_center} {width} {height}\n")