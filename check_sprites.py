from PIL import Image
import os

BASE = r'apps\web\public\assets\characters'

files = {
    'Crystalroot': 'Crystalroot.png',
    'Embervine': 'Embervine.png',
    'Frostberry': 'Frostberry.png',
    'Moonbloom': 'Moonbloom.png',
    'Shadowleaf': 'Shadowleaf.png',
    'Hoe': 'Hoe.png',
    'Watering Can': 'Watering Can.png',
    'Scythe': 'Scythe.png',
    'Basket': 'Basket.png',
    'Action Icons': 'Action Icons.png',
    'Currency Icons': 'Currency Icons.png',
    'Rarity Badges': 'Rarity Badges.png',
    'Wild Zone Materials': 'Wild Zone Materials.png',
    'Ground Tiles': 'Ground Tiles.png',
    'Common Crop Seeds': r'common crop seeds\Common Crop Seeds.png',
    'Uncommon Crop Seeds': r'Uncommon Crop Seeds\Uncommon Crop Seeds.png',
    'Rare Crop Seed': r'Rare Crop Seed\Rare Crop Seed.png',
    'Wild Zone Seeds': r'Wild Zone Seeds\Wild Zone Seeds.png',
}

for name, rel in files.items():
    path = os.path.join(BASE, rel)
    if os.path.exists(path):
        img = Image.open(path)
        print(f'{name}: {img.size[0]}x{img.size[1]}px')
    else:
        print(f'{name}: NOT FOUND ({path})')