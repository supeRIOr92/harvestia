from PIL import Image
import numpy as np
import os

BASE = r'apps\web\public\assets\characters'
path = os.path.join(BASE, r'Uncommon Crop Seeds\Uncommon Crop Seeds.png')
img = Image.open(path).convert('RGBA')

# Remove bg
arr = np.array(img)
bg = arr[0, 0, :3]
diff = np.abs(arr[:, :, :3].astype(int) - bg.astype(int))
is_bg = np.all(diff < 30, axis=2)
arr[:, :, 3] = np.where(is_bg, 0, 255)

alpha = arr[:, :, 3]
filled = np.any(alpha > 10, axis=0)

# Detect boundaries
boundaries = []
in_content = False
start = 0

for i, has_content in enumerate(filled):
    if has_content and not in_content:
        in_content = True
        start = i
    elif not has_content and in_content:
        in_content = False
        boundaries.append((start, i - 1))

if in_content:
    boundaries.append((start, len(filled) - 1))

print(f'Image size: {img.size}')
print(f'Detected {len(boundaries)} items:')
for i, (x1, x2) in enumerate(boundaries):
    print(f'  Item {i}: x={x1}-{x2}, width={x2 - x1 + 1}px')