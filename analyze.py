import time
import json

import numpy as np
import cv2
import matplotlib.pyplot as plt


class Timer:
    index = 0

    def __init__(self, name: str) -> None:
        self.number = type(self).index
        type(self).index += 1

        self.name = name

        self.stop = None
        self.start = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop = time.time()
        print(f"Time elapsed in chunk number {self.number} - {self.name}: {(self.stop - self.start):.6f}")
        return False


class Image:
    def __init__(self, path: str) -> None:
        self.image = cv2.imread(path)

        self.minimize(100)

        self.rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB) / 255
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV) / 255
        self.hsv_image[..., 0] *= 2 * np.pi

    def minimize(self, needable_size: int = 1000) -> None:
        height, width, _ = self.image.shape
        max_side = max(width, height)

        if max_side > 2 * needable_size:
            scale = needable_size / max_side

            self.image = cv2.resize(self.image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)


def analyze(image_path: str) -> None:

    with Timer("Main frame"):
        image = Image(image_path)

        hue, saturation, value = cv2.split(image.hsv_image)

        S_hist, S_vals = np.histogram(saturation, bins=100)
        S_hist = S_hist / S_hist.sum()
        S_vals = (S_vals[1:] + S_vals[:-1]) / 2

        V_hist, V_vals = np.histogram(value, bins=100)
        V_hist = V_hist / V_hist.sum()
        V_vals = (V_vals[1:] + V_vals[:-1]) / 2

        rgb_copy = image.rgb_image.copy()


    # plottting
    with Timer("Plot masks making"):
        fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(8, 8))
        
        h_unic, h_cnts = np.unique(hue, return_counts=True)
        
        hue_steps = np.linspace(0, np.pi * 2, 13)
        
        print(hue_steps)
        
        index = np.argmax(h_cnts)
        main_color = h_unic[index]
        
        min_index = np.argmin(np.abs(hue_steps - main_color))
        print(hue_steps[min_index])
        
        hue_f = hue.flatten()
        sat_f = saturation.flatten()
        val_f = value.flatten()
        
        data = {
            "hue": hue_f,
            "saturation": sat_f,
            "value": val_f
        }

        for i, iname in enumerate(data.keys()):
            for j, jname in enumerate(data.keys()):
                data[iname]
                ax[i][j].scatter(data[iname], data[jname], alpha=0.4, color="green")

    # making plot
    with Timer("Saving plot"):
        plt.savefig("grayscale_masks.png", dpi=200)

    # plottting
    with Timer("Plot HSV making"):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(8, 8))

        ax[0].imshow(hue, cmap="hsv")
        ax[1].imshow(saturation, cmap="gray")
        ax[2].imshow(value, cmap="inferno")

    # making plot
    with Timer("Saving plot"):
        plt.savefig("hsv_splitted.png", dpi=200)


if __name__ == "__main__":
    # image_file = "/home/dmitry/Pictures/pixels3.jpg"
    # image_file = "/home/dmitry/Pictures/pixels2.jpeg"
    image_file = "/home/dmitry/Pictures/Wallpapers/wallpaper1.jpg"

    analyze(image_file)
