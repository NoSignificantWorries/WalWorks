import colorsys
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def rgb_to_hsv(rgb_colors):
    """Конвертирует массив RGB цветов в HSV"""
    hsv_colors = []
    for rgb in rgb_colors:
        r, g, b = rgb / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hsv_colors.append([h * 360, s * 100, v * 100])  # В градусах и процентах
    return np.array(hsv_colors)

def hsv_to_rgb(hsv_colors):
    """Конвертирует массив HSV цветов обратно в RGB"""
    rgb_colors = []
    for hsv in hsv_colors:
        h, s, v = hsv[0] / 360, hsv[1] / 100, hsv[2] / 100
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        rgb_colors.append([r * 255, g * 255, b * 255])
    return np.array(rgb_colors).astype(int)

def get_theme_colors_hsv(image_path, num_colors=8):
    """Получение палитры с кластеризацией в HSV пространстве"""
    image = Image.open(image_path).convert('RGB')
    image = image.resize((100, 100))
    img_array = np.array(image)
    pixel_data = img_array.reshape(-1, 3)
    
    # Конвертируем в HSV для кластеризации
    hsv_data = rgb_to_hsv(pixel_data)
    
    # Кластеризация в HSV пространстве
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(hsv_data)
    
    # Получаем центры кластеров в HSV и конвертируем обратно в RGB
    hsv_palette = kmeans.cluster_centers_
    rgb_palette = hsv_to_rgb(hsv_palette)
    
    return rgb_palette, hsv_palette


def rgb_to_lab(rgb_colors):
    """Конвертирует RGB в Lab через XYZ"""
    # Сначала нормализуем RGB
    rgb_normalized = rgb_colors / 255.0
    
    # Конвертация в XYZ
    mask = rgb_normalized > 0.04045
    rgb_normalized[mask] = ((rgb_normalized[mask] + 0.055) / 1.055) ** 2.4
    rgb_normalized[~mask] = rgb_normalized[~mask] / 12.92
    
    rgb_normalized = rgb_normalized * 100
    
    # Матрица преобразования RGB to XYZ
    x = rgb_normalized[:, 0] * 0.4124 + rgb_normalized[:, 1] * 0.3576 + rgb_normalized[:, 2] * 0.1805
    y = rgb_normalized[:, 0] * 0.2126 + rgb_normalized[:, 1] * 0.7152 + rgb_normalized[:, 2] * 0.0722
    z = rgb_normalized[:, 0] * 0.0193 + rgb_normalized[:, 1] * 0.1192 + rgb_normalized[:, 2] * 0.9505
    
    # Нормализуем относительно белой точки D65
    x = x / 95.047
    y = y / 100.000
    z = z / 108.883
    
    # Конвертация XYZ в Lab
    mask = x > 0.008856
    x[mask] = x[mask] ** (1/3)
    x[~mask] = (7.787 * x[~mask]) + (16/116)
    
    mask = y > 0.008856
    y[mask] = y[mask] ** (1/3)
    y[~mask] = (7.787 * y[~mask]) + (16/116)
    
    mask = z > 0.008856
    z[mask] = z[mask] ** (1/3)
    z[~mask] = (7.787 * z[~mask]) + (16/116)
    
    L = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)
    
    return np.column_stack([L, a, b])

def get_theme_colors_lab(image_path, num_colors=8):
    """Получение палитры с кластеризацией в Lab пространстве"""
    image = Image.open(image_path).convert('RGB')
    image = image.resize((100, 100))
    img_array = np.array(image)
    pixel_data = img_array.reshape(-1, 3)
    
    # Конвертируем в Lab для кластеризации
    lab_data = rgb_to_lab(pixel_data)
    
    # Кластеризация в Lab пространстве (лучше для восприятия!)
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(lab_data)
    
    # Получаем центры кластеров в Lab
    lab_palette = kmeans.cluster_centers_
    
    return lab_palette


def analyze_colors_in_different_spaces(image_path, num_colors=8):
    """Сравнение палитр из разных цветовых пространств"""
    
    # Получаем палитры разными способами
    rgb_palette_hsv, hsv_palette = get_theme_colors_hsv(image_path, num_colors)
    lab_palette = get_theme_colors_lab(image_path, num_colors)
    
    print("🎨 СРАВНЕНИЕ ЦВЕТОВЫХ ПРОСТРАНСТВ")
    print("=" * 70)
    
    print("\n🔴 Палитра из HSV пространства (лучше для насыщенных цветов):")
    for i, (rgb, hsv) in enumerate(zip(rgb_palette_hsv, hsv_palette)):
        r, g, b = rgb
        h, s, v = hsv
        print(f"{i+1:2d}. RGB({r:3d},{g:3d},{b:3d}) | "
              f"HSV({h:3.0f}°,{s:3.0f}%,{v:3.0f}%)")
    
    print("\n🎨 Палитра из Lab пространства (лучше для восприятия):")
    for i, lab in enumerate(lab_palette):
        L, a, b = lab
        print(f"{i+1:2d}. Lab(L:{L:5.1f}, a:{a:6.1f}, b:{b:6.1f})")

def filter_by_saturation(hsv_palette, min_saturation=20):
    """Фильтрует цвета по насыщенности"""
    saturated_colors = []
    for hsv in hsv_palette:
        h, s, v = hsv
        if s >= min_saturation:
            saturated_colors.append(hsv)
    return np.array(saturated_colors)

def group_by_hue_ranges(hsv_palette, hue_ranges):
    """Группирует цвета по диапазонам оттенков"""
    groups = {name: [] for name in hue_ranges}
    
    for hsv in hsv_palette:
        h, s, v = hsv
        for name, (min_h, max_h) in hue_ranges.items():
            if min_h <= h <= max_h:
                groups[name].append(hsv)
                break
    
    return groups

# Пример использования
if __name__ == "__main__":
    image_path = "/home/dmitry/.wallpaper"
    
    # Анализ в разных пространствах
    analyze_colors_in_different_spaces(image_path)
    
    # Получаем HSV палитру для дополнительной обработки
    rgb_palette, hsv_palette = get_theme_colors_hsv(image_path)
    
    # Фильтруем по насыщенности (только яркие цвета)
    saturated_hsv = filter_by_saturation(hsv_palette, min_saturation=30)
    saturated_rgb = hsv_to_rgb(saturated_hsv)
    
    print("\n🎯 ТОЛЬКО НАСЫЩЕННЫЕ ЦВЕТА (S ≥ 30%):")
    for i, (rgb, hsv) in enumerate(zip(saturated_rgb, saturated_hsv)):
        r, g, b = rgb
        h, s, v = hsv
        print(f"{i+1:2d}. RGB({r:3d},{g:3d},{b:3d}) | "
              f"HSV({h:3.0f}°,{s:3.0f}%,{v:3.0f}%)")
    
    # Группировка по цветовым диапазонам
    hue_ranges = {
        "Красные": [0, 15],
        "Оранжевые": [15, 45],
        "Желтые": [45, 75],
        "Зеленые": [75, 165],
        "Голубые": [165, 195],
        "Синие": [195, 255],
        "Фиолетовые": [255, 285],
        "Пурпурные": [285, 345],
        "Красные2": [345, 360]
    }
    
    color_groups = group_by_hue_ranges(hsv_palette, hue_ranges)
    
    print("\n🌈 ГРУППИРОВКА ПО ЦВЕТОВЫМ ДИАПАЗОНАМ:")
    for color_name, colors in color_groups.items():
        if colors:
            print(f"{color_name:12}: {len(colors)} цветов")
