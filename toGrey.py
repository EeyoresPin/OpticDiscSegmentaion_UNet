from PIL import Image
import cv2
import os

def convert_and_binarize_masks(input_folder, output_folder):
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load the image
            image = cv2.imread(input_path)

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Save the result
            cv2.imwrite(output_path, gray_image)
            print(f"Processed: {filename}")

# Example usage
#input_masks_folder = r'Blood_Cell_img\train\masks_rgb'       # <-- Change this to your actual input folder
#output_masks_folder = r'Blood_Cell_img\train\masks_binary'   # <-- Output folder (can be new)

convert_and_binarize_masks('Blood_Cell_img/train/mask_copy', 'Blood_Cell_img/train/mask')
