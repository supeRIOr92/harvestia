from PIL import Image
import numpy as np

path = r'apps\web\public\assets\characters\Uncommon Crop Seeds\Uncommon Crop Seeds.png'
img = Image.open(path).convert('RGBA')
arr = np.array(img)

print('corner pixels:')
print('top-left [0,0]:', arr[0,0])
print('top-right [0,-1]:', arr[0,-1])
print('bottom-left [-1,0]:', arr[-1,0])
print('bottom-right [-1,-1]:', arr[-1,-1])

print('\nsamples di area kiri (sebelum content):')
for x in [50, 100, 200, 300, 400]:
    print(f' [center_y, x={x}]:', arr[arr.shape[0]//2, x])
