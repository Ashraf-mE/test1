import cv2
import os

# Function to convert YOLO format to pixel coordinates
def yolo_to_pixel_coords(image_width, image_height, x_center, y_center, width, height):
    x_center *= image_width
    y_center *= image_height
    width *= image_width
    height *= image_height
    x_min = int(x_center - width / 2)
    y_min = int(y_center - height / 2)
    x_max = int(x_center + width / 2)
    y_max = int(y_center + height / 2)
    return x_min, y_min, x_max, y_max

# Example image and label file paths
image_path = "F:/Lane-detection/datasets/llamas/grayscale_images/train/images-2014-12-22-15-18-11_mapping_RTC_to_280_left_lanes/1419290326_0370951000_gray_rect.png"
label_path = "F:/Lane-detection/datasets/llamas/labels/labels/train/YoloFormat/images-2014-12-22-15-18-11_mapping_RTC_to_280_left_lanes/1419290326_0370951000.txt"

# Read the image
image = cv2.imread(image_path)
image_height, image_width = image.shape[:2]

# Read the YOLO format label file
with open(label_path, 'r') as f:
    lines = f.readlines()

# Draw bounding boxes on the image
for line in lines:
    class_id, x_center, y_center, width, height = map(float, line.strip().split())
    x_min, y_min, x_max, y_max = yolo_to_pixel_coords(image_width, image_height, x_center, y_center, width, height)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

# Display the image with bounding boxes
cv2.imshow('Image with Bounding Boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
