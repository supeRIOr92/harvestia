from PIL import Image
import os

# Target tile size
TILE_SIZE = 64

# Folder assets
ASSETS_DIR = r"apps\web\public\assets\characters"

def resize_image(input_path, output_path, size):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    # Hitung scale ratio berdasarkan dimensi terbesar
    ratio = size / max(w, h)
    new_w = round(w * ratio)
    new_h = round(h * ratio)

    resized = img.resize((new_w, new_h), Image.NEAREST)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    resized.save(output_path, "PNG")
    print(f" {os.path.basename(input_path)}: {w}x{h} → {new_w}x{new_h}")

def process_folder(folder, target_size):
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith(".png"):
                input_path = os.path.join(root, filename)
                # Simpan ke folder baru: assets/characters-resized/
                rel_path = os.path.relpath(input_path, folder)
                output_folder = folder.replace("characters", "characters-resized")
                output_path = os.path.join(output_folder, rel_path)
                resize_image(input_path, output_path, target_size)

print(f"Resizing all assets to max {TILE_SIZE}px...")
process_folder(ASSETS_DIR, TILE_SIZE)
print("\nDone! Output: apps/web/public/assets/characters-resized/")