from colorthief import ColorThief


def color_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def print_palette(colors: list[tuple[int, int, int]]) -> None:
    for rgb in colors:
        hex_color = color_to_hex(rgb)
        block = "███" * 5
        ansi_color = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{block}\033[0m"
        
        print(f"{ansi_color} RGB{rgb} | {hex_color}")


filepath = "/home/dmitry/.wallpaper"

color_thief = ColorThief(filepath)
dominant_colors = color_thief.get_palette(color_count=16)

dominant_colors_hex = list(map(color_to_hex, dominant_colors))

# print("\n".join(dominant_colors_hex))
print_palette(dominant_colors)
