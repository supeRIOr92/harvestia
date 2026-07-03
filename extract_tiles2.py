from PIL import Image
import numpy as np
import os

OUTPUT = r'apps\web\public\assets\tiles'
os.makedirs(OUTPUT, exist_ok=True)


def save_tile(img, out_name, size=(64, 64)):
    img = img.convert('RGBA')
    resized = img.resize(size, Image.NEAREST)
    resized.save(os.path.join(OUTPUT, out_name))
    print(f'Saved: {out_name} → {size}')


def extract_content(path):
    """Crop out transparent border, return content only"""
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    if not rows.any():
        return img
    rmin, rmax = int(np.where(rows)[0][0]), int(np.where(rows)[0][-1])
    cmin, cmax = int(np.where(cols)[0][0]), int(np.where(cols)[0][-1])
    return img.crop((cmin, rmin, cmax + 1, rmax + 1))


# Grass tile
grass = extract_content(r'apps\web\public\assets\characters\grassy.png')
save_tile(grass, 'grass.png', (64, 64))

# Soil / tilled plot
soil = Image.open(r'apps\web\public\assets\characters\soil.png').convert('RGBA')
save_tile(soil, 'soil.png', (64, 64))

# Dirt
dirt = Image.open(r'apps\web\public\assets\characters\dirt.png').convert('RGBA')
save_tile(dirt, 'dirt.png', (64, 64))

# Wooden fence
wood = extract_content(r'apps\web\public\assets\characters\wooden.png')
save_tile(wood, 'fence.png', (64, 64))

# House
house = extract_content(r'apps\web\public\assets\characters\house.png')
save_tile(house, 'house.png', (192, 192))  # house lebih gede

# Stall
stall = extract_content(r'apps\web\public\assets\characters\stall.png')
save_tile(stall, 'stall.png', (128, 128))

# Tree
tree = extract_content(r'apps\web\public\assets\characters\tree.png')
save_tile(tree, 'tree.png', (64, 96))

# Character frames — 4 horizontal frames
male = Image.open(r'apps\web\public\assets\characters\male.png').convert('RGBA')
fw = male.width // 4

for i, name in enumerate(['char_down', 'char_up', 'char_left', 'char_right']):
    frame = male.crop((i * fw, 0, (i + 1) * fw, male.height))
    save_tile(frame, f'{name}.png', (40, 64))

# Crops — wheat, carrot, tomato (3 growth stages per spritesheet)
crops = {
    'wheat': r'apps\web\public\assets\characters\common crops\wheat.png',
    'carrot': r'apps\web\public\assets\characters\common crops\carrot.png',
    'tomato': r'apps\web\public\assets\characters\common crops\tomato.png',
    'corn': r'apps\web\public\assets\characters\common crops\corn.png',
    'potato': r'apps\web\public\assets\characters\common crops\potato.png',
}

for crop_name, path in crops.items():
    crop_img = Image.open(path).convert('RGBA')
    cw, ch = crop_img.size
    # Tiap crop punya 3 stage horizontal
    frame_w = cw // 3
    for stage_i, stage in enumerate(['seed', 'growing', 'mature']):
        frame = crop_img.crop((stage_i * frame_w, 0, (stage_i + 1) * frame_w, ch))
        content = extract_content.__wrapped__(frame) if hasattr(extract_content, '__wrapped__') else frame
        save_tile(frame, f'{crop_name}_{stage}.png', (48, 48))

print('\nDone! All tiles saved to:', OUTPUT)