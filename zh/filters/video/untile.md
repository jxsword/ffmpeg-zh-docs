# untile

Decompose a video made of tiled images into the individual images.

The frame rate of the output video is the frame rate of the input video multiplied by the number of tiles.

This filter does the reverse of [tile](tile.md#tile).

The filter accepts the following options:

- **`layout`** Set the grid size (i.e. the number of lines and columns). For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

## Examples

- Produce a 1-second video from a still image file made of 25 frames stacked vertically, like an analogic film reel:

  ``` text
  ffmpeg -r 1 -i image.jpg -vf untile=1x25 movie.mkv
  ```
