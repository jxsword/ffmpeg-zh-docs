# drawvg

Draw vector graphics on top of video frames, by executing a script written in a custom language called VGS (*Vector Graphics Script*).

The documentation for the language can be found in section "drawvg - Language Reference" in `drawvg-reference`. A version of this reference with rendered examples can be found at the [author's site](https://ayosec.github.io/ffmpeg-drawvg/playground/docs/langref.html).

Graphics are rendered using the [cario 2D graphics library](https://cairographics.org/).

To enable compilation of this filter, you need to configure FFmpeg with `--enable-cairo`.

## Parameters

Either `script` or `file` must be set.

| Term        | Description                                 |
|-------------|---------------------------------------------|
| `s, script` | Script source to draw the graphics.         |
| `file`      | Path of the file to load the script source. |

## Pixel Formats

Since Cairo only supports RGB images, if the input video is something else (like YUV 4:2:0), before executing the script the video is converted to a format compatible with Cairo. Then, you have to use either the [format](format.md#format) filter, or the `-pix_fmt` option, to convert it to the expected format in the output.

## Examples

- Draw the outline of an ellipse.

  ``` text
  ffmpeg -i input.webm \
      -vf 'drawvg=ellipse (w/2) (h/2) (w/3) (h/3) stroke' \
      -pix_fmt yuv420p \
      output.webm
  ```

- Draw a square rotating in the middle of the frame.

  The script for drawvg is in a file `draw.vgs`:

  ``` text
  translate (w/2) (h/2)
  rotate t
  rect -100 -100 200 200
  setcolor red@0.5
  fill
  ```

  Then:

  ``` text
  ffmpeg -i input.webm -vf 'drawvg=file=draw.vgs,format=yuv420p' output.webm
  ```
