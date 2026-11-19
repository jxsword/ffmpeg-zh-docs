# overlay_opencl

Overlay one video on top of another.

It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid. This filter requires same memory layout for all the inputs. So, format conversion may be needed.

The filter accepts the following options:

- **`x`** Set the x coordinate of the overlaid video on the main video. Default value is `0`.

- **`y`** Set the y coordinate of the overlaid video on the main video. Default value is `0`.

## Examples

- Overlay an image LOGO at the top-left corner of the INPUT video. Both inputs are yuv420p format.

  ``` text
  -i INPUT -i LOGO -filter_complex "[0:v]hwupload[a], [1:v]format=yuv420p, hwupload[b], [a][b]overlay_opencl, hwdownload" OUTPUT
  ```

- The inputs have same memory layout for color channels , the overlay has additional alpha plane, like INPUT is yuv420p, and the LOGO is yuva420p.

  ``` text
  -i INPUT -i LOGO -filter_complex "[0:v]hwupload[a], [1:v]format=yuva420p, hwupload[b], [a][b]overlay_opencl, hwdownload" OUTPUT
  ```
