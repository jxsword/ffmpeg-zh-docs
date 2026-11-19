# dilation_opencl

Apply dilation effect to the video.

This filter replaces the pixel by the local(3x3) maximum.

It accepts the following options:

- **`threshold0`**

- **`threshold1`**

- **`threshold2`**

- **`threshold3`** Limit the maximum change for each plane. Range is `[0, 65535]` and default value is `65535`. If `0`, plane will remain unchanged.

- **`coordinates`** Flag which specifies the pixel to refer to. Range is `[0, 255]` and default value is `255`, i.e. all eight pixels are used.

  Flags to local 3x3 coordinates region centered on `x`:

  1 2 3

  4 x 5

  6 7 8

## Example

- Apply dilation filter with threshold0 set to 30, threshold1 set 40, threshold2 set to 50 and coordinates set to 231, setting each pixel of the output to the local maximum between pixels: 1, 2, 3, 6, 7, 8 of the 3x3 region centered on it in the input. If the difference between input pixel and local maximum is more then threshold of the corresponding plane, output pixel will be set to input pixel + threshold of corresponding plane.

  ``` text
  -i INPUT -vf "hwupload, dilation_opencl=30:40:50:coordinates=231, hwdownload" OUTPUT
  ```
