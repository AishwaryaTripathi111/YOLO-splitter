import os
import random
import shutil
from pathlib import Path

def clean_and_split_dataset(base_path, train_pct=0.9):
    image_dir = Path(base_path) / "images"
    label_dir = Path(base_path) / "labels"

    # Step 1: Flatten image folder if nested
    print("📦 Checking and flattening image directory...")
    all_imgs = list(image_dir.rglob("*"))
    for img in all_imgs:
        if img.is_file() and img.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            if img.parent != image_dir:
                shutil.move(str(img), str(image_dir / img.name))

    # Step 2: Gather images
    img_files = [f for f in image_dir.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    print(f"🔍 Found {len(img_files)} image files.")

    if len(img_files) == 0:
        print("⚠️ No images found. Please check your /images folder.")
        return

    # Step 3: Shuffle and split
    random.shuffle(img_files)
    split_idx = int(train_pct * len(img_files))
    train_imgs = img_files[:split_idx]
    val_imgs = img_files[split_idx:]

    # Step 4: Create folders and copy files
    for group, name in [(train_imgs, "train"), (val_imgs, "val")]:
        img_out_dir = Path(base_path) / name / "images"
        lbl_out_dir = Path(base_path) / name / "labels"
        img_out_dir.mkdir(parents=True, exist_ok=True)
        lbl_out_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 Copying {len(group)} images to {name} folder...")
        for img_path in group:
            label_path = label_dir / (img_path.stem + ".txt")
            shutil.copy(img_path, img_out_dir / img_path.name)
            if label_path.exists():
                shutil.copy(label_path, lbl_out_dir / label_path.name)

    print("✅ Dataset split complete.")

# 🔧 Run the function
custom_dataset_path = "/content/custom_data"  # Update if your path is different
clean_and_split_dataset(custom_dataset_path, train_pct=0.9)
