COLORS = [
    {
        "name": "red1",
        "hex": "#ff0000",
        "hue": 0
    },
    {
        "name": "orange",
        "hex": "#ff8000",
        "hue": 30
    },
    {
        "name": "yellow",
        "hex": "#ffff00",
        "hue": 60
    },
    {
        "name": "chartreuse",
        "hex": "#80ff00",
        "hue": 90
    },
    {
        "name": "green",
        "hex": "#00ff00",
        "hue": 120
    },
    {
        "name": "spring-green",
        "hex": "#00ff80",
        "hue": 150
    },
    {
        "name": "cyan",
        "hex": "#00ffff",
        "hue": 180
    },
    {
        "name": "azure",
        "hex": "#0080ff",
        "hue": 210
    },
    {
        "name": "blue",
        "hex": "#0000ff",
        "hue": 240
    },
    {
        "name": "violet",
        "hex": "#8000ff",
        "hue": 270
    },
    {
        "name": "magenta",
        "hex": "#ff00ff",
        "hue": 300
    },
    {
        "name": "rose",
        "hex": "#ff0080",
        "hue": 330
    },
    {
        "name": "red2",
        "hex": "#ff0000",
        "hue": 360
    }
]


STANDART_THRESHOLDS_CHROMA = {
    "not-color": -0.001,
    "achromatic": 0.02,      # Полностью ахроматический - не отличим от серого
    "near-neutral": 0.06,    # Почти нейтральный - едва заметный оттенок
    "very-weak-color": 0.12, # Очень слабый цвет
    "weak-color": 0.18,     # Слабый цвет (пастельные тона)
    "medium-color": 0.30,   # Умеренный цвет
    "strong-color": 0.45,   # Сильный цвет
    "very-strong-color": 0.60, # Очень сильный цвет
    "vivid-color": 0.80,    # Яркий, насыщенный цвет
    "clear-color": 1.0
}

STANDART_THRESHOLDS_LIGHTNESS = {
    "black": -0.001,
    "very-dark": 0.20,      # Очень темный
    "dark": 0.35,           # Темный
    "medium-dark": 0.50,    # Средне-темный
    "medium": 0.65,         # Средний
    "medium-light": 0.80,   # Средне-светлый  
    "light": 0.90,          # Светлый
    "very-light": 0.95,     # Очень светлы
    "white": 1.0
}
