import os
import random
import shutil
from pathlib import Path

def split_yolo_dataset(base_path, train_pct=0.9):
    images_dir = Path(base_path) / "images"
    labels_dir = Path(base_path) / "labels"
    
    # Collect all images (jpg and png)
    img_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
    random.shuffle(img_files)

    # Split into train and val sets
    split_idx = int(train_pct * len(img_files))
    train_imgs = img_files[:split_idx]
    val_imgs = img_files[split_idx:]

    for group, name in [(train_imgs, "train"), (val_imgs, "val")]:
        img_out_dir = Path(base_path) / name / "images"
        lbl_out_dir = Path(base_path) / name / "labels"
        img_out_dir.mkdir(parents=True, exist_ok=True)
        lbl_out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nCopying {len(group)} images to {name} folder...")

        for img_path in group:
            label_path = labels_dir / (img_path.stem + ".txt")

            # Copy image file always
            shutil.copy(img_path, img_out_dir / img_path.name)
            print(f"Copied image: {img_path.name}")

            # Copy label file if it exists
            if label_path.exists():
                shutil.copy(label_path, lbl_out_dir / label_path.name)
                print(f"Copied label: {label_path.name}")
            else:
                print(f"No label for image: {img_path.name}")

    print("\n✅ Dataset split complete.")

# Example usage: adjust base_path accordingly
split_yolo_dataset("/content/custom_data", train_pct=0.9)


