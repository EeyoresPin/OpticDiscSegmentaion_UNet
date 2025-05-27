#!/usr/bin/env python3
"""
Binary Mask Class Distribution Analyzer

This script analyzes binary mask images (PNG files with 0s and 1s) to:
1. Calculate class distribution for each image
2. Generate a histogram showing distribution across all images in a folder
3. Provide summary statistics

Requirements:
- numpy
- opencv-python (cv2)
- matplotlib
- Pillow (PIL)
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import argparse
from pathlib import Path
import pandas as pd

def analyze_single_mask(image_path):
    """
    Analyze a single binary mask image and return class distribution.
    
    Args:
        image_path (str): Path to the binary mask image
        
    Returns:
        dict: Dictionary containing class distribution info
    """
    try:
        # Load image using PIL to handle various formats better
        img = Image.open(image_path)
        
        # Convert to numpy array
        mask = np.array(img)
        
        # Handle different image formats (RGB, RGBA, grayscale)
        if len(mask.shape) == 3:
            # Convert to grayscale if multi-channel
            mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        
        # Ensure binary (convert to 0s and 1s)
        mask = (mask > 0).astype(np.uint8)
        
        # Calculate class distribution
        total_pixels = mask.size
        class_1_pixels = np.sum(mask)
        class_0_pixels = total_pixels - class_1_pixels
        
        class_1_ratio = class_1_pixels / total_pixels
        class_0_ratio = class_0_pixels / total_pixels
        
        return {
            'filename': os.path.basename(image_path),
            'total_pixels': total_pixels,
            'class_0_pixels': class_0_pixels,
            'class_1_pixels': class_1_pixels,
            'class_0_ratio': class_0_ratio,
            'class_1_ratio': class_1_ratio,
            'image_shape': mask.shape
        }
        
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def analyze_folder(folder_path, output_dir=None):
    """
    Analyze all PNG files in a folder and generate statistics and visualizations.
    
    Args:
        folder_path (str): Path to folder containing PNG mask files
        output_dir (str): Directory to save output files (optional)
    """
    folder_path = Path(folder_path)
    if not folder_path.exists():
        raise ValueError(f"Folder {folder_path} does not exist")
    
    # Find all PNG files
    png_files = list(folder_path.glob("*.png"))
    if not png_files:
        raise ValueError(f"No PNG files found in {folder_path}")
    
    print(f"Found {len(png_files)} PNG files to analyze...")
    
    # Analyze each image
    results = []
    for img_path in png_files:
        result = analyze_single_mask(img_path)
        if result:
            results.append(result)
    
    if not results:
        raise ValueError("No valid mask images were processed")
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(results)
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Total images processed: {len(results)}")
    print(f"Average Blood Cell ratio: {df['class_1_ratio'].mean():.4f}")
    print(f"Std dev Blood Cell ratio: {df['class_1_ratio'].std():.4f}")
    print(f"Min Blood Cell ratio: {df['class_1_ratio'].min():.4f}")
    print(f"Max Blood Cell ratio: {df['class_1_ratio'].max():.4f}")
    print(f"Median Blood Cell ratio: {df['class_1_ratio'].median():.4f}")
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Binary Mask Class Distribution Analysis', fontsize=16, fontweight='bold')
    
    # 1. Histogram of Blood Cell ratios
    axes[0, 0].hist(df['class_1_ratio'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribution of Blood Cell Ratios')
    axes[0, 0].set_xlabel('Blood Cell Ratio')
    axes[0, 0].set_ylabel('Number of Images')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Bar plot of individual images (showing top 20 if too many)
    display_df = df.head(20) if len(df) > 20 else df
    x_pos = range(len(display_df))
    axes[0, 1].bar(x_pos, display_df['class_1_ratio'], alpha=0.7, color='lightcoral')
    axes[0, 1].set_title(f'Blood Cell Ratio per Image {"(First 20)" if len(df) > 20 else ""}')
    axes[0, 1].set_xlabel('Image Index')
    axes[0, 1].set_ylabel('Blood Cell Ratio')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Box plot
    axes[1, 0].boxplot([df['class_0_ratio'], df['class_1_ratio']], 
                       labels=['Backround', 'Blood Cell'])
    axes[1, 0].set_title('Box Plot of Class Ratios')
    axes[1, 0].set_ylabel('Ratio')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Scatter plot of class ratios
    axes[1, 1].scatter(df['class_0_ratio'], df['class_1_ratio'], alpha=0.6, color='green')
    axes[1, 1].set_title('Backround vs Blood Cell Ratios')
    axes[1, 1].set_xlabel('Backround Ratio')
    axes[1, 1].set_ylabel('Blood Cell Ratio')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save outputs if output directory is specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save plot
        plot_path = output_dir / 'class_distribution_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {plot_path}")
        
        # Save detailed CSV
        csv_path = output_dir / 'detailed_analysis.csv'
        df.to_csv(csv_path, index=False)
        print(f"Detailed analysis saved to: {csv_path}")
        
        # Save summary statistics
        summary_path = output_dir / 'summary_statistics.txt'
        with open(summary_path, 'w') as f:
            f.write("Binary Mask Class Distribution Analysis\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total images processed: {len(results)}\n")
            f.write(f"Average Blood Cell ratio: {df['class_1_ratio'].mean():.4f}\n")
            f.write(f"Std dev Blood Cell ratio: {df['class_1_ratio'].std():.4f}\n")
            f.write(f"Min Blood Cell ratio: {df['class_1_ratio'].min():.4f}\n")
            f.write(f"Max Blood Cell ratio: {df['class_1_ratio'].max():.4f}\n")
            f.write(f"Median Blood Cell ratio: {df['class_1_ratio'].median():.4f}\n\n")
            
            # Add quartile information
            f.write("Quartile Information:\n")
            f.write(f"25th percentile: {df['class_1_ratio'].quantile(0.25):.4f}\n")
            f.write(f"75th percentile: {df['class_1_ratio'].quantile(0.75):.4f}\n")
        
        print(f"Summary statistics saved to: {summary_path}")
    
    plt.show()
    
    return df

def main():
    """Main function to handle command line arguments and run analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze binary mask images for class distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mask_analyzer.py /path/to/masks/
  python mask_analyzer.py /path/to/masks/ --output /path/to/output/
  python mask_analyzer.py /path/to/masks/ -o results/
        """
    )
    
    parser.add_argument('folder_path', 
                       help='Path to folder containing PNG mask files')
    parser.add_argument('-o', '--output', 
                       help='Output directory for saving results (optional)')
    
    args = parser.parse_args()
    
    try:
        df = analyze_folder(args.folder_path, args.output)
        print(f"\nAnalysis complete! Processed {len(df)} images.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())