# chromahold

Remove all color information for all colors except for certain one.

The filter accepts the following options:

- **`color`** The color which will not be replaced with neutral chroma.

- **`similarity`** Similarity percentage with the above color. 0.01 matches only the exact key color, while 1.0 matches everything.

- **`blend`** Blend percentage. 0.0 makes pixels either fully gray, or not gray at all. Higher values result in more preserved color.

- **`yuv`** Signals that the color passed is already in YUV instead of RGB.

  Literal colors like "green" or "red" don't make sense with this enabled anymore. This can be used to pass exact YUV values as hexadecimal numbers.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
