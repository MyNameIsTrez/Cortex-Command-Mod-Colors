import os
from PIL import Image
from collections import Counter


colors = {} # Dictionary of tuples

for root, dirs, files in os.walk(os.path.join(os.getcwd(), "Input")): # "cwd" means current working directory.
    for file in files:
        if file.lower().endswith(('.png', '.bmp')):
            filePath = os.path.join(root, file)
            try:
                image = Image.open(filePath).convert("RGB") # Not sure if converting to RGB is necessary for PNGs or BMPs.
            except OSError as err:
                print("Skipped file due to RLE encoded BMP:\n" + filePath)
            for color in image.getdata():
                colors[color] = colors.get(color, 0) + 1 # "color" is a tuple and the key, ", 0" sets a default index of 0.

with open("Output.txt", "w") as out:
    mostCommon = Counter(colors).most_common()
    for pair in mostCommon:
        out.write(str(pair) + "\n")