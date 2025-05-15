import os
import random
import shutil
from pathlib import Path

def split_yolo_dataset(base_path, train_pct=0.9):
    images_dir = Path(base_path) / "images"
    labels_dir = Path(base_path) / "labels"
    
    img_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
    random.shuffle(img_files)

    split_idx = int(train_pct * len(img_files))
    train_imgs = img_files[:split_idx]
    val_imgs = img_files[split_idx:]

    for group, name in [(train_imgs, "train"), (val_imgs, "val")]:
        img_out_dir = Path(base_path) / name / "images"
        lbl_out_dir = Path(base_path) / name / "labels"
        img_out_dir.mkdir(parents=True, exist_ok=True)
        lbl_out_dir.mkdir(parents=True, exist_ok=True)

        for img_path in group:
            label_path = labels_dir / (img_path.stem + ".txt")
            if label_path.exists():
                shutil.copy(img_path, img_out_dir / img_path.name)
                shutil.copy(label_path, lbl_out_dir / label_path.name)

    print("✅ Dataset split complete.")

split_yolo_dataset("/content/custom_data", train_pct=0.9)

