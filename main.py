import os, json
from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


plotMostCommon = True # When set to False it'll plot the least common colors.
blacklistColors = ((93, 158, 225), (255, 0, 255), (79, 79, 79))
plotColorCount = 25


palette = Image.open("palette.bmp").getpalette()
colors = {}

for i in range(0, len(palette), 3):
    color = (palette[i], palette[i+1], palette[i+2])
    colors[color] = 0


inputPath = os.path.join(os.getcwd(), "Input") # "cwd" means current working directory.

for root, dirs, files in os.walk(inputPath):
    for file in files:
        if file.lower().endswith((".png", ".bmp")):
            filePath = os.path.join(root, file)

            try:
                image = Image.open(filePath).convert("RGB") # Not sure if converting to RGB is necessary for PNGs or BMPs.
            except OSError as err:
                print("Skipped file due to RLE compressed BMP:\n" + filePath)

            imgColors = {}
            for color in image.getdata():
                count = colors.get(color)
                seenInImg = imgColors.get(color) != None
                if count != None and seenInImg == False:
                    colors[color] = count + 1 # "color" is a tuple and the key.
                    imgColors[color] = True


with open("output.json", "w") as fp:
    mostCommon = Counter(colors).most_common() # most_common() sorts by value of a dictionary.
    json.dump(mostCommon, fp)
    # print(len(mostCommon))


for blacklistColor in blacklistColors: # Remove colors that are so common they make the chart very skewed and hard to read.
    colors.pop(blacklistColor, None) # "None" prevents KeyError that's thrown when the blacklistColor isn't in the dictionary.


mostCommonBlacklisted = Counter(colors).most_common() # most_common() sorts by value of a dictionary.
if plotMostCommon == True:
    clrs = mostCommonBlacklisted[:plotColorCount] # Gets the most common colors.
else:
    clrs = mostCommonBlacklisted[-plotColorCount:] # Gets the least common colors.
rgbColors, rgbCounts = zip(*clrs)

y_pos = np.arange(len(rgbColors))
plt.xticks(y_pos, rgbColors)

colorsNormalized = [tuple(rgbValue / 255 for rgbValue in rgbColor) for rgbColor in rgbColors]
plt.bar(y_pos, rgbCounts, color=colorsNormalized)

plt.gcf().autofmt_xdate() # Rotates the x-axis labels by 45 degrees so they don't overlap.

plt.ylabel("Count")

modCount = len([name for name in os.listdir("Input") if os.path.isdir(os.path.join(inputPath, name))])
plt.title("How often the {} {} common CC palette colors were used in {} mods".format(plotColorCount, "most" if plotMostCommon else "least", modCount))

plt.show()