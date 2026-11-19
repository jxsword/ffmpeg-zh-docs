# sr_amf

Upscale (size increasing) for the input video using AMD Advanced Media Framework library for hardware acceleration. Use advanced algorithms for upscaling with higher output quality. Setting the output width and height works in the same way as for the [scale](scale.md#scale) filter.

The filter accepts the following options:

- **`w`**

- **`h`** Set the output video dimension expression. Default value is the input dimension.

  Allows for the same expressions as the [scale](scale.md#scale) filter.

- **`algorithm`** Sets the algorithm used for scaling:

  | Term         | Description                         |
  |--------------|-------------------------------------|
  | \<bilinear\> | Bilinear                            |
  | \<bicubic\>  | Bicubic                             |
  | \<sr1-0\>    | Video SR1.0 This is a default value |
  | \<point\>    | Point                               |
  | \<sr1-1\>    | Video SR1.1                         |

- **`sharpness`** Control hq scaler sharpening. The value is a float in the range of \[0.0, 2.0\]

- **`format`** Controls the output pixel format. By default, or if none is specified, the input pixel format is used.

- **`keep-ratio`** Force the scaler to keep the aspect ratio of the input image when the output size has a different aspect ratio. Default value is false.

- **`fill`** Specifies whether the output image outside the region of interest, which does not fill the entire output surface should be filled with a solid color.

## Examples

- Scale input to 720p, keeping aspect ratio and ensuring the output is yuv420p.

  ``` text
  sr_amf=-2:720:format=yuv420p
  ```

- Upscale to 4K with algorithm video SR1.1.

  ``` text
  sr_amf=4096:2160:algorithm=sr1-1
  ```
