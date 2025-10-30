from pathlib import Path

import numpy as np
import cv2

import data as d


image_path = "~/.wallpaper"
image_path = Path(image_path).expanduser()


raw_image = cv2.imread(image_path)

needable_size = 1000

height, width, _ = raw_image.shape
max_side = max(width, height)

if max_side > 2 * needable_size:
    scale = needable_size / max_side

    raw_image = cv2.resize(raw_image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

HEIGHT, WIDTH = raw_image.shape[0], raw_image.shape[1]
TOTAL_PIXELS = raw_image.shape[0] * raw_image.shape[1]

print(HEIGHT, WIDTH)
print(TOTAL_PIXELS)


rgb_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB) / 255
hsv_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV) / 255
hsv_image[..., 0] *= np.pi * 2

image_lab = cv2.cvtColor(raw_image, cv2.COLOR_BGR2LAB).astype(np.float32)
image_lab[..., 0] = image_lab[..., 0] / 255.0
image_lab[..., 1] = (image_lab[..., 1] - 128.0) / 127.0
image_lab[..., 2] = (image_lab[..., 2] - 128.0) / 127.0

chroma = np.hypot(image_lab[..., 1], image_lab[..., 2]) / np.sqrt(2)
chroma = chroma.reshape((*chroma.shape, 1))


layer_names = ["red", "green", "blue", "hue", "saturation", "value", "L", "a", "b", "chroma"]
data = np.concatenate([rgb_image, hsv_image, image_lab, chroma], axis=-1)

chroma_keys = list(d.STANDART_THRESHOLDS_CHROMA.keys())[1:]
lightness_keys = list(d.STANDART_THRESHOLDS_LIGHTNESS)

print(chroma_keys)
print(lightness_keys)

chroma_thresholds_items = list(d.STANDART_THRESHOLDS_CHROMA.items())
for i in range(len(chroma_thresholds_items) - 1):
    p1, p2 = chroma_thresholds_items[i], chroma_thresholds_items[i + 1]
