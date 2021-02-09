import os, json
from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


blacklistedColors = ((255, 0, 255), (93, 158, 225)) # Removes background magenta and sky blue.
plotColorCount = 25

# countColorOncePerImage = True # If set to False it'll mean the huge, brown terrain sprites dominate. If set to false, the black outlines of sprites dominate.
# plotMostCommon = True # When set to False it'll plot the least common colors.


palette = Image.open("palette.bmp").getpalette()
inputFolderPath = os.path.join(os.getcwd(), "Input") # "cwd" means current working directory.
modCount = len([name for name in os.listdir("Input") if os.path.isdir(os.path.join(inputFolderPath, name))])
colors = {}


def loadPaletteColors():
    global colors

    colors = {}
    for i in range(0, len(palette), 3):
        color = (palette[i], palette[i+1], palette[i+2])
        colors[color] = 1 # Setting it to 0 would mean the unused colors would never appear on a graph.


def addImageColors(countColorOncePerImage):
    global colors

    for root, dirs, files in os.walk(inputFolderPath):
        for file in files:
            if file.lower().endswith((".png", ".bmp")):
                filePath = os.path.join(root, file)

                try:
                    image = Image.open(filePath).convert("RGB") # Not sure if converting to RGB is necessary for PNGs or BMPs.
                except OSError:
                    print("Skipped file due to RLE compressed BMP:\n" + filePath)

                if countColorOncePerImage:
                    imgColors = {}

                for color in image.getdata():
                    count = colors.get(color)
                    
                    if countColorOncePerImage:
                        if imgColors.get(color) != None:
                            continue
                    
                    if count != None:
                        colors[color] = count + 1 # "color" is a tuple and the key.
                        
                        if countColorOncePerImage:
                            imgColors[color] = True


# def writeResults():
#     global colors
#     with open("output.json", "w") as outFile:
#         mostCommon = Counter(colors).most_common() # most_common() sorts by value of a dictionary.
#         json.dump(mostCommon, outFile)


def removeBlacklistedColors():
    global colors
    for blacklistedColor in blacklistedColors: # Remove colors that are so common they make the chart very skewed and hard to read.
        colors.pop(blacklistedColor, None) # "None" prevents KeyError that's thrown when the blacklistedColor isn't in the dictionary.


def drawSubplot(ax, countColorOncePerImage, plotMostCommon):
    global colors

    mostCommonBlacklisted = Counter(colors).most_common() # most_common() sorts by value of a dictionary.

    if plotMostCommon == True:
        clrs = mostCommonBlacklisted[:plotColorCount] # Gets the most common colors.
    else:
        clrs = mostCommonBlacklisted[-plotColorCount:] # Gets the least common colors.

    rgbColors, rgbCounts = zip(*clrs)

    colorsNormalized = [tuple(rgbValue / 255 for rgbValue in rgbColor) for rgbColor in rgbColors]

    y_pos = np.arange(len(rgbColors))

    # plt.xticks(y_pos, rgbColors)
    # plt.bar(y_pos, rgbCounts, color=colorsNormalized)

    ax.bar(y_pos, rgbCounts, color=colorsNormalized)

    ax.set_title("How often the {} {} common CC palette colors were used in {} mods{}".format(
        plotColorCount,
        "most" if plotMostCommon else "least",
        modCount,
        "\n(If a color appears more than once in an image it isn't counted again)" if countColorOncePerImage else ""))

    ax.axis("off")

    # plt.gcf().autofmt_xdate() # Rotates the x-axis labels by 45 degrees so they don't overlap.
    # plt.ylabel("Count")
    # plt.title("How often the {} {} common CC palette colors were used in {} mods{}".format(
    #     plotColorCount,
    #     "most" if plotMostCommon else "least",
    #     modCount,
    #     "\n(A color can only be counted once per image)" if countColorOncePerImage else ""))

fig, axes = plt.subplots(2, 2)

for x in range(2):
    for y in range(2):
        loadPaletteColors()
        addImageColors(countColorOncePerImage = x == 1)
        removeBlacklistedColors()
        drawSubplot(axes[y, x], countColorOncePerImage = x == 1, plotMostCommon = y == 0)

plt.show()