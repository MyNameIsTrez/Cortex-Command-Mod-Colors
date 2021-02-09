import os, json
from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


blacklistColors = ((93, 158, 225), (255, 0, 255), (79, 79, 79))
plotColorCount = 25


colors = {}

inputPath = os.path.join(os.getcwd(), "Input") # "cwd" means current working directory.

for root, dirs, files in os.walk(inputPath):
    for file in files:
        if file.lower().endswith((".png", ".bmp")):
            filePath = os.path.join(root, file)

            try:
                image = Image.open(filePath).convert("RGB") # Not sure if converting to RGB is necessary for PNGs or BMPs.
            except OSError as err:
                print("Skipped file due to RLE compressed BMP:\n" + filePath)

            for color in image.getdata():
                colors[color] = colors.get(color, 0) + 1 # "color" is a tuple and the key, ", 0" sets a default index of 0.


with open("output.json", "w") as fp:
    mostCommon = Counter(colors).most_common()
    json.dump(mostCommon, fp)


for blacklistColor in blacklistColors: # Remove colors that are so common they make the chart very skewed and hard to read.
    colors.pop(blacklistColor, None) # "None" prevents KeyError that's thrown when the blacklistColor isn't in the dictionary.


rgbColors, rgbCounts = zip(*Counter(colors).most_common()[:plotColorCount]) # most_common() sorts by value of a dictionary. [:plotColorCount] shows only the most common colors.

y_pos = np.arange(len(rgbColors))
plt.xticks(y_pos, rgbColors)

colorsNormalized = [tuple(rgbValue / 255 for rgbValue in rgbColor) for rgbColor in rgbColors]
plt.bar(y_pos, rgbCounts, color=colorsNormalized)

plt.gcf().autofmt_xdate() # Rotates the x-axis labels by 45 degrees so they don't overlap.

plt.ylabel("Count")

modCount = len([name for name in os.listdir("Input") if os.path.isdir(os.path.join(inputPath, name))])
plt.title(f"How often the {plotColorCount} most common colors were used in {modCount} mods")

plt.show()