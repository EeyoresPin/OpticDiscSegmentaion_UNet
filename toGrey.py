from PIL import Image
import cv2
import os
import numpy as np

def convert_to_binary_masks(input_folder, output_folder):
    """
    Convert images to binary masks where 0 stays 0 and all values > 0 become 1.
    This creates binary masks where 0 = background, 1 = foreground.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    processed_count = 0
    error_count = 0

    # Process all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            
            # Change output extension to .png for consistency
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.png")

            try:
                # Load the image
                image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
                
                if image is None:
                    print(f"Error: Could not load {filename}")
                    error_count += 1
                    continue

                # Create binary mask: all values > 0 become 1, 0 stays 0
                binary_mask = np.where(image > 0, 1, 0).astype(np.uint8)

                # Save the result as PNG
                cv2.imwrite(output_path, binary_mask)
                print(f"Processed: {filename} -> {base_name}.png")
                processed_count += 1

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                error_count += 1

    print(f"\nConversion complete!")
    print(f"Successfully processed: {processed_count} files")
    if error_count > 0:
        print(f"Errors encountered: {error_count} files")

def convert_to_binary_masks_pil(input_folder, output_folder):
    """
    Alternative version using PIL instead of OpenCV.
    Convert images to binary masks where 0 stays 0 and all values > 0 become 1.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    processed_count = 0
    error_count = 0

    # Process all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            
            # Change output extension to .png for consistency
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.png")

            try:
                # Load the image with PIL
                with Image.open(input_path) as img:
                    # Convert to grayscale if not already
                    if img.mode != 'L':
                        gray_img = img.convert('L')
                    else:
                        gray_img = img
                    
                    # Convert to numpy array for processing
                    gray_array = np.array(gray_img)
                    
                    # Create binary mask: all values > 0 become 1, 0 stays 0
                    binary_array = np.where(gray_array > 0, 1, 0).astype(np.uint8)
                    
                    # Convert back to PIL Image and save
                    binary_img = Image.fromarray(binary_array, mode='L')
                    binary_img.save(output_path, 'PNG')
                    
                    print(f"Processed: {filename} -> {base_name}.png")
                    processed_count += 1

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                error_count += 1

    print(f"\nConversion complete!")
    print(f"Successfully processed: {processed_count} files")
    if error_count > 0:
        print(f"Errors encountered: {error_count} files")

# Example usage - choose one of the functions below:

# Using OpenCV (recommended for speed)
convert_to_binary_masks('Final data/Final data/New folder/Mask', 'Final data/Final data/New folder/Mask_Binary')

# Alternative using PIL (uncomment to use instead)
# convert_to_binary_masks_pil('Final data/Final data/New folder/Mask', 'Final data/Final data/New folder/Mask_Binary')

# You can also call it with different folders:
# convert_to_binary_masks('path/to/input', 'path/to/output')