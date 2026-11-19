# colorkey

RGB colorspace color keying. This filter operates on 8-bit RGB format frames by setting the alpha component of each pixel which falls within the similarity radius of the key color to 0. The alpha value for pixels outside the similarity radius depends on the value of the blend option.

The filter accepts the following options:

- **`color`** Set the color for which alpha will be set to 0 (full transparency). See section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default is `black`.

- **`similarity`** Set the radius from the key color within which other colors also have full transparency. The computed distance is related to the unit fractional distance in 3D space between the RGB values of the key color and the pixel's color. Range is 0.01 to 1.0. 0.01 matches within a very small radius around the exact key color, while 1.0 matches everything. Default is `0.01`.

- **`blend`** Set how the alpha value for pixels that fall outside the similarity radius is computed. 0.0 makes pixels either fully transparent or fully opaque. Higher values result in semi-transparent pixels, with greater transparency the more similar the pixel color is to the key color. Range is 0.0 to 1.0. Default is `0.0`.

## Examples

- Make every green pixel in the input image transparent:

  ``` text
  ffmpeg -i input.png -vf colorkey=green out.png
  ```

- Overlay a greenscreen-video on top of a static background image.

  ``` text
  ffmpeg -i background.png -i video.mp4 -filter_complex "[1:v]colorkey=0x3BBD1E:0.3:0.2[ckout];[0:v][ckout]overlay[out]" -map "[out]" output.flv
  ```

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
