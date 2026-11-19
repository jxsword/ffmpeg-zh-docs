# format

Convert the input video to one of the specified pixel formats. Libavfilter will try to pick one that is suitable as input to the next filter.

It accepts the following parameters:

- **`pix_fmts`** A '\|'-separated list of pixel format names, such as "pix_fmts=yuv420p\|monow\|rgb24".

- **`color_spaces`** A '\|'-separated list of color space names, such as "color_spaces=bt709\|bt470bg\|bt2020nc".

- **`color_ranges`** A '\|'-separated list of color range names, such as "color_ranges=tv\|pc".

- **`alpha_modes`** A '\|'-separated list of color range names, such as "alpha_modes=straight\|premultiplied".

## Examples

- Convert the input video to the \<yuv420p\> format

  ``` text
  format=pix_fmts=yuv420p
  ```

  Convert the input video to any of the formats in the list

  ``` text
  format=pix_fmts=yuv420p|yuv444p|yuv410p
  ```
