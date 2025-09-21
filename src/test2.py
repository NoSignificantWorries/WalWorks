import os
import json

import cv2
import numpy as np
import matplotlib.pyplot as plt


class Colors:
    def __init__(self, path: str | None = None):
        self.palette = {}
        self.color_names = []
        if path is not None:
            self.load(path)
    
    def __getitem__(self, idx: str | int) -> dict:
        return self.palette[idx]
    
    def load(self, path: str) -> None:
        with open(path, "r") as json_file:
            data = json.load(json_file)
            for color in data:
                self.add(name=color["name"],
                         hex_col=color["hex"],
                         hue=color["hue"])
                self.color_names.append(color["name"])
    
    def add(self, name: str, hex_col: str, hue: int) -> None:
        if name in self.palette.keys():
            return
        
        color = {
            "name": name,
            "hex": hex_col,
            "hue": hue
        }
        self.palette[name] = color
        self.palette[hex_col] = color
        self.palette[hue] = color
        
        self.color_names.append(name)


class Colorizer:
    def __init__(self, path: str, colors: Colors) -> None:
        self.path = path
        self.base_colors = colors

        image_obj = cv2.imread(path)
        self.rgb_image = cv2.cvtColor(image_obj, cv2.COLOR_BGR2RGB) / 255

        self.hsv_image = cv2.cvtColor(image_obj, cv2.COLOR_BGR2HSV).astype(np.float64)
        self.hsv_image[..., 0] /= 179
        self.hsv_image[..., 0] *= 360
        self.hsv_image[..., 1:] /= 255

        # self.lab_image = cv2.cvtColor(image_obj, cv2.COLOR_BGR2LAB).astype(np.float64)
    
    def draw_color_lines(self, ax, colors):
        for name in colors.color_names:
            color = colors[name]
            ax.axvline(x=color["hue"], color=color["hex"], linestyle="--", linewidth=2)
    
    def body(self):
        
        # step = 3
        # start = (step - 1) // 2
        # hsv_image_1_3 = self.hsv_image[start::step, start::step, :]
        
        _, ax = plt.subplots(nrows=3, ncols=1, figsize=(24, 24))

        # ===============================================================
        hue = self.hsv_image[..., 0]
        hs, counts = np.unique(hue, return_counts=True)

        lax = ax[0]

        lax.bar(hs, counts,
               color="green",
               edgecolor='black', linewidth=1.2, alpha=0.8)
        
        self.draw_color_lines(lax, self.base_colors)
        
        # ===============================================================
        
        lax = ax[1]

        # ===============================================================
        
        lax = ax[2]

        # ===============================================================

        plt.legend()
        
        plt.savefig("hist_hue.png", dpi=300)
        

def main(filepath: str) -> None:
    colors = Colors("src/base-colors.json")

    colorizer = Colorizer(filepath, colors)
    
    colorizer.body()
    

if __name__ == "__main__":
    filepath = "/home/dmitry/.wallpaper"
    # filepath = "/home/dmitry/Pictures/pixels3.jpg"
    # filepath = "/home/dmitry/Pictures/ref1.jpg"
    
    main(filepath)
