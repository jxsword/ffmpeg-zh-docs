# noformat

Force libavfilter not to use any of the specified pixel formats for the input to the next filter.

It accepts the following parameters:

- **`pix_fmts`** A '\|'-separated list of pixel format names, such as pix_fmts=yuv420p\|monow\|rgb24".

## Examples

- Force libavfilter to use a format different from \<yuv420p\> for the input to the vflip filter:

  ``` text
  noformat=pix_fmts=yuv420p,vflip
  ```

- Convert the input video to any of the formats not contained in the list:

  ``` text
  noformat=yuv420p|yuv444p|yuv410p
  ```
