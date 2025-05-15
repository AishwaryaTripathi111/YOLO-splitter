import os
import random
import shutil
from pathlib import Path

def split_yolo_dataset(base_path, train_pct=0.9):
    images_dir = Path(base_path) / "images"
    labels_dir = Path(base_path) / "labels"

    # Collect image files with various extensions
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
    img_files = []
    for ext in extensions:
        img_files.extend(images_dir.rglob(ext))  # rglob to support nested dirs too

    if len(img_files) == 0:
        print("⚠️ No image files found in:", images_dir)
        return

    random.shuffle(img_files)
    split_idx = int(train_pct * len(img_files))
    train_imgs = img_files[:split_idx]
    val_imgs = img_files[split_idx:]

    # Output folders
    for group, name in [(train_imgs, "train"), (val_imgs, "val")]:
        img_out_dir = Path(base_path) / name / "images"
        lbl_out_dir = Path(base_path) / name / "labels"
        img_out_dir.mkdir(parents=True, exist_ok=True)
        lbl_out_dir.mkdir(parents=True, exist_ok=True)

        print(f"📦 Copying {len(group)} images to {name} folder...")

        for img_path in group:
            label_path = labels_dir / (img_path.stem + ".txt")
            shutil.copy(img_path, img_out_dir / img_path.name)
            if label_path.exists():
                shutil.copy(label_path, lbl_out_dir / label_path.name)

    print("✅ Dataset split complete.")


# 🔥 Run the function
split_yolo_dataset("/content/custom_data", train_pct=0.9)
