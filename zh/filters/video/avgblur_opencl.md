# avgblur_opencl

Apply average blur filter.

The filter accepts the following options:

- **`sizeX`** Set horizontal radius size. Range is `[1, 1024]` and default value is `1`.

- **`planes`** Set which planes to filter. Default value is `0xf`, by which all planes are processed.

- **`sizeY`** Set vertical radius size. Range is `[1, 1024]` and default value is `0`. If zero, `sizeX` value will be used.

## Example

- Apply average blur filter with horizontal and vertical size of 3, setting each pixel of the output to the average value of the 7x7 region centered on it in the input. For pixels on the edges of the image, the region does not extend beyond the image boundaries, and so out-of-range coordinates are not used in the calculations.

  ``` text
  -i INPUT -vf "hwupload, avgblur_opencl=3, hwdownload" OUTPUT
  ```
