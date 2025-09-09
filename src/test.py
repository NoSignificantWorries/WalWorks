from PIL import Image
import numpy as np

filepath = "/home/dmitry/.wallpaper"

image = Image.open(filepath)
pixels = np.array(image)

x, y = 100, 50
color = pixels[y, x]
print(pixels.shape)
print(f"Цвет в точке ({x},{y}): {color}")

