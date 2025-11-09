COLORS = [
    ['#c7c7c7', '#2f93f5', '#6cb24e', '#ffc63a', '#ff922c', '#fb5a53', '#e2216b'],
    ['#ae20c0', '#ff1810', '#f6908e', '#ffd6d3', '#ffdcb4', '#ffc680', '#da9142'],
    ['#9f6636', '#252525', '#363636', '#575658', '#737373', '#9a9a9a', '#b2b2b2'],
    ['#dbdbdb', '#f0f0f0', '#fefefe']
]

PALETTE = [c for row in COLORS for c in row]

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

PALETTE_RGB = [hex_to_rgb(c) for c in PALETTE]

FIRST_COLOR_POSITION = (430, 2270)
COLOR_INTERVAL = 80

START_POSITION = (250, 800)
SIZE = 800
PIXEL_INTERVAL = 8 # int(SIZE / 10)
IGNORE_SOLO_PIXELS = False