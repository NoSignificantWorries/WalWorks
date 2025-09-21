from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def img_to_hsv(rgb_image):
    r, g, b = rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2]

    M = np.max(rgb_image, axis=2)
    m = np.min(rgb_image, axis=2)
    C = M - m
    
    V = M
    S = np.zeros_like(V)
    mask = V != 0
    S[mask] = C[mask] / V[mask]

    H = np.zeros_like(V)
    
    mask_r = (M == r) & (C != 0)
    mask_g = (M == g) & (C != 0)
    mask_b = (M == b) & (C != 0)
    
    H[mask_r] = ((g[mask_r] - b[mask_r]) / C[mask_r]) % 6
    H[mask_g] = ((b[mask_g] - r[mask_g]) / C[mask_g]) + 2
    H[mask_b] = ((r[mask_b] - g[mask_b]) / C[mask_b]) + 4
    
    H = H * 60
    H[H < 0] += 360
    
    return np.stack([H, S, V], axis=-1)

filepath = "/home/dmitry/.wallpaper"

image = Image.open(filepath)
rgb_pixels = np.array(image) / 255
hsv_pixels = img_to_hsv(rgb_pixels)

x, y = 100, 50
rgb = rgb_pixels[y, x]
hsv = hsv_pixels[y, x]
print(rgb_pixels.shape)
print(f"Цвет в точке ({x}, {y}): {rgb}")
print(f"Цвет в точке ({x}, {y}): {hsv}")


_, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))
ax[0].imshow(hsv_pixels[..., 0])
ax[1].imshow(hsv_pixels[..., 1])
ax[2].imshow(hsv_pixels[..., 2])

plt.savefig("res.png", dpi=300)

