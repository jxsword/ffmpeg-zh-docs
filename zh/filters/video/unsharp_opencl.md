# unsharp_opencl

Sharpen or blur the input video.

It accepts the following parameters:

- **`luma_msize_x, lx`** Set the luma matrix horizontal size. Range is `[1, 23]` and default value is `5`.

- **`luma_msize_y, ly`** Set the luma matrix vertical size. Range is `[1, 23]` and default value is `5`.

- **`luma_amount, la`** Set the luma effect strength. Range is `[-10, 10]` and default value is `1.0`.

  Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

- **`chroma_msize_x, cx`** Set the chroma matrix horizontal size. Range is `[1, 23]` and default value is `5`.

- **`chroma_msize_y, cy`** Set the chroma matrix vertical size. Range is `[1, 23]` and default value is `5`.

- **`chroma_amount, ca`** Set the chroma effect strength. Range is `[-10, 10]` and default value is `0.0`.

  Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

All parameters are optional and default to the equivalent of the string '5:5:1.0:5:5:0.0'.

## Examples

- Apply strong luma sharpen effect:

  ``` text
  -i INPUT -vf "hwupload, unsharp_opencl=luma_msize_x=7:luma_msize_y=7:luma_amount=2.5, hwdownload" OUTPUT
  ```

- Apply a strong blur of both luma and chroma parameters:

  ``` text
  -i INPUT -vf "hwupload, unsharp_opencl=7:7:-2:7:7:-2, hwdownload" OUTPUT
  ```
