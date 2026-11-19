# colorkey_opencl

RGB colorspace color keying.

The filter accepts the following options:

- **`color`** The color which will be replaced with transparency.

- **`similarity`** Similarity percentage with the key color.

  0.01 matches only the exact key color, while 1.0 matches everything.

- **`blend`** Blend percentage.

  0.0 makes pixels either fully transparent, or not transparent at all.

  Higher values result in semi-transparent pixels, with a higher transparency the more similar the pixels color is to the key color.

## Examples

- Make every semi-green pixel in the input transparent with some slight blending:

  ``` text
  -i INPUT -vf "hwupload, colorkey_opencl=green:0.3:0.1, hwdownload" OUTPUT
  ```
