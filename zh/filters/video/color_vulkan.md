# color_vulkan

Video source that creates a Vulkan frame of a solid color. Useful for benchmarking, or overlaying.

It accepts the following parameters:

- **`color`** The color to use. Either a name, or a hexadecimal value. The default value is `black`.

- **`size`** The size of the output frame. Default value is `1920x1080`.

- **`rate`** The framerate to output at. Default value is `60` frames per second.

- **`duration`** The video duration. Default value is `-0.000001`.

- **`sar`** The video signal aspect ratio. Default value is `1/1`.

- **`format`** The pixel format of the output Vulkan frames. Default value is `yuv444p`.

- **`out_range`** Set the output YCbCr sample range.

  This allows the autodetected value to be overridden as well as allows forcing a specific value used for the output and encoder. If not specified, the range depends on the pixel format. Possible values:

  | Term                | Description                                      |
  |---------------------|--------------------------------------------------|
  | `auto/unknown`    | Choose automatically.                            |
  | `jpeg/full/pc`    | Set full range (0-255 in case of 8-bit luma).    |
  | `mpeg/limited/tv` | Set "MPEG" range (16-235 in case of 8-bit luma). |
