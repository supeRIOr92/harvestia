from PIL import Image
import os

OUTPUT_DIR = r'apps\web\public\assets\tiles'
os.makedirs(OUTPUT_DIR, exist_ok=True)

TILE_OUT_SIZE = 64  # final size per tile


def extract_and_save(src_path, out_name, crop_box):
    img = Image.open(src_path).convert('RGBA')
    tile = img.crop(crop_box)
    tile = tile.resize((TILE_OUT_SIZE, TILE_OUT_SIZE), Image.NEAREST)
    out_path = os.path.join(OUTPUT_DIR, out_name)
    tile.save(out_path)
    print(f'Saved: {out_name} ({crop_box})')


# grassy.png — 1024x1024, konten di cell tengah grid 4x4 (256px per cell)
# Cell [1,1] = x:256-512, y:256-512
# Cell [1,2] = x:512-768, y:256-512
# Cell [2,1] = x:256-512, y:512-768
# Cell [2,2] = x:512-768, y:512-768
extract_and_save(
    r'apps\web\public\assets\characters\grassy.png',
    'grass.png',
    (256, 256, 512, 512)
)

extract_and_save(
    r'apps\web\public\assets\characters\grassy.png',
    'grass2.png',
    (512, 256, 768, 512)
)

# soil.png — 1254x1254, extract area tengah
# Cek dulu area mana yang ada isinya
soil = Image.open(r'apps\web\public\assets\characters\soil.png').convert('RGBA')
sw, sh = soil.size
print(f'soil.png size: {sw}x{sh}')

# Ambil center tile
center_x = sw // 2
center_y = sh // 2
half = 256

extract_and_save(
    r'apps\web\public\assets\characters\soil.png',
    'soil.png',
    (center_x - half, center_y - half, center_x + half, center_y + half)
)

# wooden fence
extract_and_save(
    r'apps\web\public\assets\characters\wooden.png',
    'fence.png',
    (256, 256, 512, 512)
)

# Character sprites — male.png 500x500, 4 frames horizontal (125px each)
char = Image.open(r'apps\web\public\assets\characters\male.png').convert('RGBA')
frame_w = 500 // 4  # 125px per frame

for i, name in enumerate(['char_down', 'char_up', 'char_left', 'char_right']):
    tile = char.crop((i * frame_w, 0, (i + 1) * frame_w, 500))
    tile = tile.resize((48, 64), Image.NEAREST)
    out_path = os.path.join(OUTPUT_DIR, f'{name}.png')
    tile.save(out_path)
    print(f'Saved: {name}.png')

print('\nDone! Tiles saved to:', OUTPUT_DIR)