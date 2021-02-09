# Cortex-Command-Mod-Colors

Counts the number of each of the 256 CC palette colors used by mods thrown into the `Input` folder and outputs the result to `Output.txt`.

It only counts the colors from `BMPs` and `PNGs`. You'll need to unzip the mods yourself and you can't leave any zips in the `Input` folder behind.

The reading of [RLE](https://en.wikipedia.org/wiki/Run-length_encoding) compressed BMPs is currently not supported, so those files will just be skipped.