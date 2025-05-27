import os
import shutil
import yaml
from pathlib import Path

def merge_datasets(dataset_paths, output_dir):
    # Create output directory structure
    os.makedirs(os.path.join(output_dir, 'train', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'valid', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'valid', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', 'labels'), exist_ok=True)

    # Initialize merged data with single class
    merged_data = {
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': 1,
        'names': ['human'],
        'roboflow': {
            'workspace': 'merged-dataset',
            'project': 'merged-thermal-dataset',
            'version': 1,
            'license': 'CC BY 4.0',
            'url': ''
        }
    }

    # Process each dataset
    for dataset_path in dataset_paths:
        # Read the data.yaml file
        with open(os.path.join(dataset_path, 'data.yaml'), 'r') as f:
            data = yaml.safe_load(f)
        
        # Copy files for each split
        for split in ['train', 'valid', 'test']:
            src_img_dir = os.path.join(dataset_path, split, 'images')
            src_label_dir = os.path.join(dataset_path, split, 'labels')
            dst_img_dir = os.path.join(output_dir, split, 'images')
            dst_label_dir = os.path.join(output_dir, split, 'labels')

            # Copy images
            if os.path.exists(src_img_dir):
                for img_file in os.listdir(src_img_dir):
                    if img_file.endswith(('.jpg', '.jpeg', '.png')):
                        src_path = os.path.join(src_img_dir, img_file)
                        dst_path = os.path.join(dst_img_dir, img_file)
                        # Handle filename conflicts
                        if os.path.exists(dst_path):
                            base, ext = os.path.splitext(img_file)
                            dst_path = os.path.join(dst_img_dir, f"{base}_{Path(dataset_path).name}{ext}")
                        shutil.copy2(src_path, dst_path)

            # Copy and update labels
            if os.path.exists(src_label_dir):
                for label_file in os.listdir(src_label_dir):
                    if label_file.endswith('.txt'):
                        src_path = os.path.join(src_label_dir, label_file)
                        dst_path = os.path.join(dst_label_dir, label_file)
                        # Handle filename conflicts
                        if os.path.exists(dst_path):
                            base, ext = os.path.splitext(label_file)
                            dst_path = os.path.join(dst_label_dir, f"{base}_{Path(dataset_path).name}{ext}")
                        
                        # Read and update label file
                        with open(src_path, 'r') as f:
                            lines = f.readlines()
                        
                        # Update all class indices to 0 (human)
                        updated_lines = []
                        for line in lines:
                            parts = line.strip().split()
                            if len(parts) >= 5:  # Ensure line has class index and coordinates
                                parts[0] = '0'  # Set class index to 0 (human)
                                updated_lines.append(' '.join(parts) + '\n')
                        
                        # Write updated label file
                        with open(dst_path, 'w') as f:
                            f.writelines(updated_lines)

    # Write merged data.yaml
    with open(os.path.join(output_dir, 'data.yaml'), 'w') as f:
        yaml.dump(merged_data, f, default_flow_style=False)

    print(f"Dataset merged successfully into {output_dir}")
    print(f"Total classes: {merged_data['nc']}")
    print(f"Classes: {merged_data['names']}")

if __name__ == "__main__":
    # List of dataset paths
    datasets = [
        "Pedestrians-Detection-1",
        "People-1",
        "PersonDection-5",
        "PersonDection-9",
        "RemoteSurveillanceThermal-7"
    ]
    
    # Output directory
    output_dir = "merged_thermal_dataset"
    
    # Merge datasets
    merge_datasets(datasets, output_dir) 