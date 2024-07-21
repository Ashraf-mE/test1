import os
import json
import cv2

# Paths to your dataset
labels_path = "C:/Users/mohammad asfraf/OneDrive/Desktop/Temporaty/datasets/labels"
images_path = "C:/Users/mohammad asfraf/OneDrive/Desktop/Temporaty/datasets/data"
output_labels_path = "C:/Users/mohammad asfraf/OneDrive/Desktop/Temporaty/datasets/YoloFormat"

# Create output directory if it doesn't exist
os.makedirs(output_labels_path, exist_ok=True)

# Function to convert to YOLO format
def convert_to_yolo_format(image_width, image_height, box):
    x_center = (box[0] + box[2]) / 2.0 / image_width
    y_center = (box[1] + box[3]) / 2.0 / image_height
    width = (box[2] - box[0]) / image_width
    height = (box[3] - box[1]) / image_height
    return x_center, y_center, width, height

# Loop through all JSON files
for label_file in os.listdir(labels_path):
    if label_file.endswith(".json"):
        with open(os.path.join(labels_path, label_file), 'r') as f:
            data = json.load(f)

        # Corresponding image
        image_file = label_file.replace('.json', '_gray_rect.png')
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        # Output label file in YOLO format
        yolo_label_file = os.path.join(output_labels_path, label_file.replace('.json', '.txt'))

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

