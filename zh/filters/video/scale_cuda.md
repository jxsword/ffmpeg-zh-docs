# scale_cuda

Scale (resize) and convert (pixel format) the input video, using accelerated CUDA kernels. Setting the output width and height works in the same way as for the [scale](scale.md#scale) filter.

The filter accepts the following options:

- **`w`**

- **`h`** Set the output video dimension expression. Default value is the input dimension.

  Allows for the same expressions as the [scale](scale.md#scale) filter.

- **`interp_algo`** Sets the algorithm used for scaling:

  - **\<nearest\>** Nearest neighbour

    Used by default if input parameters match the desired output.

  - **\<bilinear\>** Bilinear

  - **\<bicubic\>** Bicubic

    This is the default.

  - **\<lanczos\>** Lanczos

- **`format`** Controls the output pixel format. By default, or if none is specified, the input pixel format is used.

  The filter does not support converting between YUV and RGB pixel formats.

- **`passthrough`** If set to 0, every frame is processed, even if no conversion is necessary. This mode can be useful to use the filter as a buffer for a downstream frame-consumer that exhausts the limited decoder frame pool.

  If set to 1, frames are passed through as-is if they match the desired output parameters. This is the default behaviour.

- **`use_filters`** If set to 1, filter with a generic weight LUT instead of using fixed-function shader kernels. May be faster or slower depending on the hardware. A value of `auto` (the default) enables this automatically when required for correct anti-aliasing when downscaling.

- **`param`** Algorithm-Specific parameter.

  Affects the curves of the bicubic algorithm.

- **`force_original_aspect_ratio`**

- **`force_divisible_by`** Work the same as the identical [scale](scale.md#scale) filter options.

- **`reset_sar`** Works the same as the identical [scale](scale.md#scale) filter option.

## Examples

- Scale input to 720p, keeping aspect ratio and ensuring the output is yuv420p.

  ``` text
  scale_cuda=-2:720:format=yuv420p
  ```

- Upscale to 4K using nearest neighbour algorithm.

  ``` text
  scale_cuda=4096:2160:interp_algo=nearest
  ```

- Don't do any conversion or scaling, but copy all input frames into newly allocated ones. This can be useful to deal with a filter and encode chain that otherwise exhausts the decoders frame pool.

  ``` text
  scale_cuda=passthrough=0
  ```
