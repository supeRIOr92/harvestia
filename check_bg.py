from PIL import Image
import numpy as np

img = Image.open(r'apps\web\public\assets\characters\grassy.png').convert('RGBA')
arr = np.array(img)
print('top-left:', arr[0,0])
print('top-right:', arr[0,-1])
print('bottom-left:', arr[-1,0])
print('bottom-right:', arr[-1,-1])
print('center:', arr[512,512])
