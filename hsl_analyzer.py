#!/usr/bin/env python3
import sys
import math
from pathlib import Path
from collections import defaultdict
from PIL import Image


class ColorPaletteGenerator:
    def __init__(self, filepath, colors=8, max_side=1000, color_thresholds=12, lightness_thresholds=10, chroma_thresholds=10):
        self.ref_white = (95.047, 100.000, 108.883)

        try:
            self.img = Image.open(filepath)
            self.img = self.img.convert('RGB')
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

        self.W, self.H = self.img.size
        self.colors_cnt = colors

        self.color_thresholds = color_thresholds
        self.hue_step = math.pi * 2 / self.color_thresholds
        
        self.lightness_thresholds = lightness_thresholds
        self.lightness_step = 1 / self.lightness_thresholds
        self.chroma_thresholds = chroma_thresholds
        self.chroma_step = chroma_thresholds

        self.pixels = []
        self.by_hue = [[] for _ in range(color_thresholds)]
        self.by_lightness = [[] for _ in range(lightness_thresholds)]
        self.by_chroma = [[] for _ in range(chroma_thresholds)]
        self.compress_image(max_side)
    
    def compress_image(self, T):
        a, b = max(self.W, self.H), min(self.W, self.H)
        
        if a <= T:
            for y in range(self.H):
                for x in range(self.W):
                    self.pixels.append(self.img.getpixel((x, y)))
            return
        
        a_step = (a - T) // (T - 1)
        
        new_b = (b * T) // a
        b_step = (b - new_b) // (new_b - 1)
        
        new_w, w_step, new_h, h_step = (T, a_step, new_b, b_step) if self.W > self.H else (new_b, b_step, T, a_step)

        idx = 0
        x, y = 0, 0
        xi, yi = 0, 0
        while yi < new_h:
            xi = 0
            x = 0
            while xi < new_w:
                r, g, b = self.img.getpixel((x, y))
                h = self.rgb_to_hue(r, g, b)
                h = self.value_to_id(h, self.hue_step)
                l, c = self.rgb_to_lc(r, g, b)
                l = self.value_to_id(l, self.lightness_step)
                c = self.value_to_id(c, self.chroma_step)
                
                print(h, l, c)
                
                color = (r, g, b, h, l, c)
                
                self.by_hue[h].append(color)
                self.by_lightness[l].append(color)
                self.by_chroma[c].append(color)
                
                self.pixels.append(color)

                idx += 1
                xi += 1
                x += w_step

            yi += 1
            y += h_step   
        
        self.W, self.H = new_w, new_h
    
    def rgb_to_hue(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        
        if max_val == min_val:
            h = 0.0
        else:
            d = max_val - min_val
            
            if max_val == r:
                h = (g - b) / d + (6.0 if g < b else 0.0)
            elif max_val == g:
                h = (b - r) / d + 2.0
            else:
                h = (r - g) / d + 4.0
            h /= 6.0
        
        return h * math.pi * 2
    
    def rgb_to_xyz(self, r, g, b):
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        
        # Inverse sRGB companding
        r = r if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
        g = g if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
        b = b if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
        
        # Convert to XYZ using sRGB matrix
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        return (x * 100.0, y * 100.0, z * 100.0)
    
    def xyz_to_lc(self, x, y, z):
        # Normalize by reference white
        x /= self.ref_white[0]
        y /= self.ref_white[1]
        z /= self.ref_white[2]
        
        # Nonlinear transformation
        def f(t):
            if t > (6/29) ** 3:
                return t ** (1/3.0)
            else:
                return (1/3.0) * ((29/6.0) ** 2) * t + (4/29.0)
        
        fx = f(x)
        fy = f(y)
        fz = f(z)
        
        L = 116.0 * fy - 16.0
        a = 500.0 * (fx - fy)
        b = 200.0 * (fy - fz)
        
        L /= 100
        a /= 128
        b /= 128
        
        L = max(0.0, min(1.0, L))
        a = max(-1.0, min(1.0, a))
        b = max(-1.0, min(1.0, b))
        
        c = math.sqrt(a * a + b * b) / math.sqrt(2)
        
        return (L, c)
    
    def rgb_to_lc(self, r, g, b):
        x, y, z = self.rgb_to_xyz(r, g, b)
        return self.xyz_to_lc(x, y, z)
    
    def value_to_id(self, value, step):
        rel_position = value / step
        rel_position_floored =  math.floor(rel_position)

        if rel_position >= rel_position_floored + 0.5:
            return rel_position_floored + 1
        return rel_position_floored
    
    def make_palette(self):
        for h_zone in self.by_hue:
            print(len(h_zone))

    def print_palette(self, palette):
        ...

if __name__ == "__main__":
    img_path = Path("~/.wallpaper").expanduser()
    generator = ColorPaletteGenerator(img_path, max_side=600, color_thresholds=12)
    
    generator.make_palette()
