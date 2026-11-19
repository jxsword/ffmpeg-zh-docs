# unsharp

Sharpen or blur the input video.

It accepts the following parameters:

- **`luma_msize_x, lx`** Set the luma matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.

- **`luma_msize_y, ly`** Set the luma matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.

- **`luma_amount, la`** Set the luma effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5.

  Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

  Default value is 1.0.

- **`chroma_msize_x, cx`** Set the chroma matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.

- **`chroma_msize_y, cy`** Set the chroma matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.

- **`chroma_amount, ca`** Set the chroma effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5.

  Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

  Default value is 0.0.

- **`alpha_msize_x, ax`** Set the alpha matrix horizontal size. It must be an odd integer between 3 and 23. The default value is 5.

- **`alpha_msize_y, ay`** Set the alpha matrix vertical size. It must be an odd integer between 3 and 23. The default value is 5.

- **`alpha_amount, aa`** Set the alpha effect strength. It must be a floating point number, reasonable values lay between -1.5 and 1.5.

  Negative values will blur the input video, while positive values will sharpen it, a value of zero will disable the effect.

  Default value is 0.0.

All parameters are optional and default to the equivalent of the string '5:5:1.0:5:5:0.0'.

## Examples

- Apply strong luma sharpen effect:

  ``` text
  unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=2.5
  ```

- Apply a strong blur of both luma and chroma parameters:

  ``` text
  unsharp=7:7:-2:7:7:-2
  ```
