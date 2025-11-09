import os
from time import sleep
from settings import *
from PIL import Image
import numpy as np

current_color_page = 0

def click(x, y):
    os.system(f'adb shell input tap {x} {y}')

def swipe(x1, y1, x2, y2, duration=100):
    os.system(f'adb shell input swipe {x1} {y1} {x2} {y2} {duration}')

def next_color_page():
    swipe(FIRST_COLOR_POSITION[0] + 200, FIRST_COLOR_POSITION[1], FIRST_COLOR_POSITION[0], FIRST_COLOR_POSITION[1])

def swipe_left():
    swipe(FIRST_COLOR_POSITION[0], FIRST_COLOR_POSITION[1], FIRST_COLOR_POSITION[0] + 200, FIRST_COLOR_POSITION[1])

def go_to_color_page(index):
    global current_color_page

    while current_color_page < index:
        next_color_page()
        current_color_page += 1
        sleep(0.1)

    while current_color_page > index:
        swipe_left()
        current_color_page -= 1
        sleep(0.1)

def select_color(color):
    index = PALETTE_RGB.index(color)
    go_to_color_page(index // 7)
    click(FIRST_COLOR_POSITION[0] + (index % 7) * COLOR_INTERVAL, FIRST_COLOR_POSITION[1])
    sleep(0.1)

def get_palette():
    palette_img = Image.new('P', (1, 1))
    flat = []
    for (r, g, b) in PALETTE_RGB:
        flat.extend([r, g, b])
    flat += [0] * (256 * 3 - len(flat))
    palette_img.putpalette(flat)
    return palette_img

def setupImage(image_path):
    image = Image.open(image_path).convert('RGBA')
    image = image.resize((SIZE[0] // PIXEL_INTERVAL, SIZE[1] // PIXEL_INTERVAL), Image.NEAREST)

    arr = np.array(image)  # shape (H, W, 4)
    alpha = arr[..., 3]  # shape (H, W)

    mapped = image.convert('RGB').quantize(palette=get_palette(), dither=0).convert('RGBA')
    mapped.putalpha(Image.fromarray(alpha))
    
    mapped.save('mapped.png')
    return mapped


def extractLines(image, vertically=False):
    width, height = image.size

    if vertically:
        bound1 = width
        bound2 = height
    else:
        bound1 = height
        bound2 = width
    
    lines = {}
    nbLinesToDraw = 0

    for i in range(0, bound1):
        lineColor = None
        for j in range(0, bound2):
            if vertically:
                r, g, b, a = image.getpixel((i, j))
                currentPosition = (i * PIXEL_INTERVAL + START_POSITION[0], j * PIXEL_INTERVAL + START_POSITION[1])
            else:
                r, g, b, a = image.getpixel((j, i))
                currentPosition = (j * PIXEL_INTERVAL + START_POSITION[0], i * PIXEL_INTERVAL + START_POSITION[1])
            
            if a == 0:
                r, g, b = (0, 0, 0)

            if lineColor == None:
                lineColor = (r, g, b)
                lineStart = currentPosition
            elif lineColor != (r, g, b):
                if lineColor not in lines:
                    lines[lineColor] = []
                if (IGNORE_SOLO_PIXELS and lineStart != lineEnd) or not IGNORE_SOLO_PIXELS:
                    lines[lineColor].append([lineStart, lineEnd])
                nbLinesToDraw += 1
                lineColor = (r, g, b)
                lineStart = currentPosition
            lineEnd = currentPosition
        
        if lineColor not in lines:
            lines[lineColor] = []
        if (IGNORE_SOLO_PIXELS and lineStart != lineEnd) or not IGNORE_SOLO_PIXELS:
                lines[lineColor].append([lineStart, lineEnd])
        nbLinesToDraw += 1
        lineColor = None

    return lines, nbLinesToDraw

def extractPixelLinesToDraw(image):
    drawVerticallyLines, nbLinesVertical = extractLines(image, True)
    drawHorizontallyLines, nbLinesHorizontal = extractLines(image, False)
    if nbLinesHorizontal <= nbLinesVertical:
        return drawHorizontallyLines, nbLinesHorizontal
    return drawVerticallyLines, nbLinesVertical


def drawImage(image_path):
    image = setupImage(image_path)
    pixelLinesToDraw, nbLinesToDraw = extractPixelLinesToDraw(image)
    pixelLinesToDraw = dict(sorted(pixelLinesToDraw.items(), key=lambda item: -len(item[1])))

    del pixelLinesToDraw[(0, 0, 0)]

    input("Appuyez sur Entrée une fois l'application ouverte et prête...")

    n = 0
    for key, value in pixelLinesToDraw.items():
        print(f'Color : {key} {n}/{nbLinesToDraw} {n/nbLinesToDraw*100:.2f}%')
        select_color(key)
        for j in value:
            start = j[0]
            end = j[1]
            swipe(start[0], start[1], end[0], end[1], duration=1)
        n += len(value)
    print("100%")


if __name__ == '__main__':
    image_path = input("Chemin vers l'image: ")
    drawImage(image_path)