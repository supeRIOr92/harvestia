from PIL import Image
import numpy as np
import os

BASE = r'apps\web\public\assets\characters'
OUT = r'apps\web\public\assets\tiles'
os.makedirs(OUT, exist_ok=True)


def remove_bg(arr, tolerance=30):
    existing_alpha = arr[:, :, 3]
    if np.any(existing_alpha < 255):
        return arr

    bg_color = arr[0, 0, :3]
    diff = np.abs(arr[:, :, :3].astype(int) - bg_color.astype(int))
    is_bg = np.all(diff < tolerance, axis=2)

    result = arr.copy()
    result[:, :, 3] = np.where(is_bg, 0, 255)
    return result


def crop_centered(img, out_size=64, padding=6):
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)

    if not rows.any():
        return Image.new('RGBA', (out_size, out_size), (0, 0, 0, 0))

    rmin, rmax = int(np.where(rows)[0][0]), int(np.where(rows)[0][-1])
    cmin, cmax = int(np.where(cols)[0][0]), int(np.where(cols)[0][-1])

    content = img.crop((cmin, rmin, cmax + 1, rmax + 1))
    cw, ch = content.size

    max_dim = out_size - padding * 2
    scale = min(max_dim / cw, max_dim / ch)
    nw = max(1, round(cw * scale))
    nh = max(1, round(ch * scale))
    scaled = content.resize((nw, nh), Image.NEAREST)

    canvas = Image.new('RGBA', (out_size, out_size), (0, 0, 0, 0))
    canvas.paste(scaled, ((out_size - nw) // 2, (out_size - nh) // 2), scaled)
    return canvas


def detect_item_boundaries(arr, axis='x', gap_threshold=10):
    """Detect boundaries antara item dalam spritesheet berdasarkan kolom kosong"""
    alpha = arr[:, :, 3]
    if axis == 'x':
        filled = np.any(alpha > 10, axis=0)  # per kolom
    else:
        filled = np.any(alpha > 10, axis=1)  # per baris

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

    return boundaries


def single(rel, out_name, size=64, padding=4):
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  NOT FOUND: {rel}')
        return

    img = Image.open(path).convert('RGBA')
    arr = remove_bg(np.array(img))
    result = crop_centered(Image.fromarray(arr), out_size=size, padding=padding)
    result.save(os.path.join(OUT, out_name))
    print(f'  {out_name}')


def split_horizontal(rel, out_prefix, n_items, out_size=64, padding=6, min_width=10):
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  NOT FOUND: {rel}')
        return

    img = Image.open(path).convert('RGBA')
    arr = remove_bg(np.array(img), tolerance=40)  # naikin tolerance untuk file ini
    img_clean = Image.fromarray(arr)
    h = img.height

    alpha = arr[:, :, 3]
    filled = np.any(alpha > 10, axis=0)

    boundaries = []
    in_content = False
    start = 0

    for i, has_content in enumerate(filled):
        if has_content and not in_content:
            in_content = True
            start = i
        elif not has_content and in_content:
            in_content = False
            if (i - 1 - start) >= min_width:  # filter noise
                boundaries.append((start, i - 1))

    if in_content and (len(filled) - 1 - start) >= min_width:
        boundaries.append((start, len(filled) - 1))

    print(f'  {os.path.basename(rel)}: detected {len(boundaries)} items (expected {n_items})')

    if len(boundaries) != n_items:
        w = img.width
        fw = w // n_items
        boundaries = [(i * fw, (i + 1) * fw - 1) for i in range(n_items)]
        print(f'  Using equal split fallback: {fw}px per item')

    for i, (x1, x2) in enumerate(boundaries):
        frame = img_clean.crop((x1, 0, x2 + 1, h))
        result = crop_centered(frame, out_size=out_size, padding=padding)
        result.save(os.path.join(OUT, f'{out_prefix}_{i}.png'))
        print(f'  {out_prefix}_{i}.png')

def split_grid(rel, out_prefix, cols, rows, out_size=64, padding=6):
    """Split spritesheet grid cols x rows"""
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  NOT FOUND: {rel}')
        return

    img = Image.open(path).convert('RGBA')
    arr = remove_bg(np.array(img))
    img_clean = Image.fromarray(arr)
    w, h = img.size
    fw = w // cols
    fh = h // rows

    for r in range(rows):
        for c in range(cols):
            frame = img_clean.crop((c * fw, r * fh, (c + 1) * fw, (r + 1) * fh))
            result = crop_centered(frame, out_size=out_size, padding=padding)
            result.save(os.path.join(OUT, f'{out_prefix}_{r}_{c}.png'))
            print(f'  {out_prefix}_{r}_{c}.png')


def stages_autodetect(rel, name, out_size=64, padding=6):
    """3 stage crop dengan auto-detect boundaries"""
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  NOT FOUND: {rel}')
        return

    img = Image.open(path).convert('RGBA')
    arr = remove_bg(np.array(img))
    img_clean = Image.fromarray(arr)
    h = img.height

    boundaries = detect_item_boundaries(arr, axis='x')
    stage_names = ['seed', 'growing', 'mature']

    if len(boundaries) != 3:
        # Fallback equal split
        w = img.width
        fw = w // 3
        boundaries = [(i * fw, (i + 1) * fw - 1) for i in range(3)]
        print(f'  {name}: fallback equal split ({fw}px per stage)')
    else:
        print(f'  {name}: auto-detected 3 stages')

    for i, (x1, x2) in enumerate(boundaries):
        frame = img_clean.crop((x1, 0, x2 + 1, h))
        result = crop_centered(frame, out_size=out_size, padding=padding)
        result.save(os.path.join(OUT, f'{name}_{stage_names[i]}.png'))
        print(f'  {name}_{stage_names[i]}.png')


# ── GROUND TILES ──────────────────────────────
print('=== GROUND TILES ===')
single('grassy.png', 'grass.png', 64, 2)
single('soil.png', 'soil.png', 64, 2)
single('dirt.png', 'dirt.png', 64, 2)
single('sand.png', 'sand.png', 64, 2)
single('moss.png', 'moss.png', 64, 2)
single('Water Tile.png', 'water.png', 64, 2)
split_grid('Ground Tiles.png', 'ground', cols=2, rows=2, out_size=64)

# ── STRUCTURES ────────────────────────────────
print('\n=== STRUCTURES ===')
single('house.png', 'house.png', 192, 4)
single('stall.png', 'stall.png', 128, 4)
single('tree.png', 'tree.png', 80, 4)
single('flower.png', 'flower.png', 48, 4)
single('Trees Large Vegetation.png', 'trees_large.png', 128, 4)
single('Spawn Point Indicator.png', 'spawn_point.png', 64, 4)
split_grid('Decorative Elements.png', 'deco', cols=2, rows=2, out_size=64)

# ── FENCES ────────────────────────────────────
print('\n=== FENCES ===')
for i in range(1, 5):
    single(f'wooden{i if i > 1 else ""}.png', f'fence{i}.png', 64, 4)

# ── COMMON CROPS ──────────────────────────────
print('\n=== COMMON CROPS ===')
for crop in ['wheat', 'carrot', 'tomato', 'corn', 'potato']:
    stages_autodetect(fr'common crops\{crop}.png', crop)

# ── UNCOMMON CROPS ────────────────────────────
print('\n=== UNCOMMON CROPS ===')
for crop in ['sunflower', 'pepper', 'pumpkin', 'blueberry']:
    stages_autodetect(fr'uncommos crops\{crop}.png', crop)

# ── RARE CROPS ────────────────────────────────
print('\n=== RARE CROPS ===')
stages_autodetect(r'rare crops\mushroom.png', 'mushroom')

# ── WILD ZONE CROPS ───────────────────────────
print('\n=== WILD ZONE CROPS ===')
for crop in ['Crystalroot', 'Embervine', 'Frostberry', 'Moonbloom', 'Shadowleaf']:
    stages_autodetect(f'{crop}.png', crop.lower())

# ── SEEDS ─────────────────────────────────────
print('\n=== SEEDS ===')
split_horizontal(r'common crop seeds\Common Crop Seeds.png', 'seed_common', n_items=5, out_size=48)
split_horizontal(r'Uncommon Crop Seeds\Uncommon Crop Seeds.png', 'seed_uncommon', n_items=4, out_size=64, padding=4)
single(r'Rare Crop Seed\Rare Crop Seed.png', 'seed_rare.png', 48, 4)
split_horizontal(r'Wild Zone Seeds\Wild Zone Seeds.png', 'seed_wild', n_items=5, out_size=48)

# ── TOOLS ─────────────────────────────────────
print('\n=== TOOLS ===')
split_horizontal('Hoe.png', 'tool_hoe', n_items=5, out_size=48)
split_horizontal('Watering Can.png', 'tool_watering_can', n_items=5, out_size=48)
split_horizontal('Scythe.png', 'tool_scythe', n_items=5, out_size=48)
split_horizontal('Basket.png', 'tool_basket', n_items=5, out_size=48)

# ── UI & ICONS ────────────────────────────────
print('\n=== UI & ICONS ===')
split_horizontal('Action Icons.png', 'icon_action', n_items=4, out_size=48)
split_horizontal('Currency Icons.png', 'icon_currency', n_items=2, out_size=48)
split_horizontal('Rarity Badges.png', 'icon_rarity', n_items=6, out_size=48)
split_horizontal('Wild Zone Materials.png', 'wild_material', n_items=5, out_size=48)

# ── CHARACTERS ────────────────────────────────
print('\n=== CHARACTERS ===')
for gender, prefix in [('male', 'char'), ('female', 'char_f')]:
    img = Image.open(os.path.join(BASE, f'{gender}.png')).convert('RGBA')
    arr_char = remove_bg(np.array(img), tolerance=40)
    img_clean = Image.fromarray(arr_char)
    fw = img.width // 4

    for i, d in enumerate(['down', 'up', 'left', 'right']):
        frame = img_clean.crop((i * fw, 0, (i + 1) * fw, img.height))
        result = crop_centered(frame, out_size=64, padding=8)
        result.save(os.path.join(OUT, f'{prefix}_{d}.png'))
        print(f'  {prefix}_{d}.png')

single('npc.png', 'npc.png', 64, 4)

print(f'\n=== ALL DONE === Output: {OUT}')