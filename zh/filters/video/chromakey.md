# chromakey

YUV colorspace color/chroma keying.

The filter accepts the following options:

- **`color`** The color which will be replaced with transparency.

- **`similarity`** Similarity percentage with the key color.

  0.01 matches only the exact key color, while 1.0 matches everything.

- **`blend`** Blend percentage.

  0.0 makes pixels either fully transparent, or not transparent at all.

  Higher values result in semi-transparent pixels, with a higher transparency the more similar the pixels color is to the key color.

- **`yuv`** Signals that the color passed is already in YUV instead of RGB.

  Literal colors like "green" or "red" don't make sense with this enabled anymore. This can be used to pass exact YUV values as hexadecimal numbers.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.

## Examples

- Make every green pixel in the input image transparent:

  ``` text
  ffmpeg -i input.png -vf chromakey=green out.png
  ```

- Overlay a greenscreen-video on top of a static black background.

  ``` text
  ffmpeg -f lavfi -i color=c=black:s=1280x720 -i video.mp4 -shortest -filter_complex "[1:v]chromakey=0x70de77:0.1:0.2[ckout];[0:v][ckout]overlay[out]" -map "[out]" output.mkv
  ```
