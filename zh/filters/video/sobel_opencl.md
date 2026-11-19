# sobel_opencl

Apply the Sobel operator (<https://en.wikipedia.org/wiki/Sobel_operator>) to input video stream.

The filter accepts the following option:

- **`planes`** Set which planes to filter. Default value is `0xf`, by which all planes are processed.

- **`scale`** Set value which will be multiplied with filtered result. Range is `[0.0, 65535]` and default value is `1.0`.

- **`delta`** Set value which will be added to filtered result. Range is `[-65535, 65535]` and default value is `0.0`.

## Example

- Apply sobel operator with scale set to 2 and delta set to 10

  ``` text
  -i INPUT -vf "hwupload, sobel_opencl=scale=2:delta=10, hwdownload" OUTPUT
  ```
