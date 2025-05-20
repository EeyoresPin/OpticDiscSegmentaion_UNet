import os
import argparse

def find_images(directory, img_directory, output_file, recursive=False):
    # Common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.TIF', '.tif']
    
    # List to store image paths
    image_paths = []
    
    # Get the absolute path of the directory to use as reference
    abs_directory = os.path.abspath(directory)
    
    # Walk through directory
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if file has an image extension
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    # Get full path
                    full_path = os.path.join(root, file)
                    # Convert to relative path
                    rel_path = os.path.relpath(full_path, abs_directory)
                    image_paths.append(rel_path)
    else:
        # Non-recursive version - just check files in the top directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
                # Convert to relative path
                rel_path = os.path.relpath(file_path, abs_directory)
                image_paths.append(rel_path)
    
    # Write paths to output file
    with open(output_file, 'w') as f:
        for path in image_paths:
            #f.write(f"{img_directory}/{path} ")
            #f.write(f"{directory}/{path}\n")
            f.write(f"{path}\n")
    
    print(f"Found {len(image_paths)} images. Relative paths written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a text file with relative paths to all images in a directory')
    parser.add_argument('directory', help='Directory to search for images')
    parser.add_argument('img_directory', help='Di')
    parser.add_argument('output_file', help='Output text file to write paths to')
    parser.add_argument('-r', '--recursive', action='store_true', help='Search subdirectories recursively')
    
    args = parser.parse_args()
    
    find_images(args.directory, args.img_directory, args.output_file, args.recursive)