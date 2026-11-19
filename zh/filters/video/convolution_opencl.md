# convolution_opencl

Apply convolution of 3x3, 5x5, 7x7 matrix.

The filter accepts the following options:

- **`0m`**

- **`1m`**

- **`2m`**

- **`3m`** Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed numbers. Default value for each plane is `0 0 0 0 1 0 0 0 0`.

- **`0rdiv`**

- **`1rdiv`**

- **`2rdiv`**

- **`3rdiv`** Set multiplier for calculated value for each plane. If unset or 0, it will be sum of all matrix elements. The option value must be a float number greater or equal to `0.0`. Default value is `1.0`.

- **`0bias`**

- **`1bias`**

- **`2bias`**

- **`3bias`** Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. The option value must be a float number greater or equal to `0.0`. Default value is `0.0`.

## Examples

- Apply sharpen:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0, hwdownload" OUTPUT
  ```

- Apply blur:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1/9:1/9:1/9:1/9, hwdownload" OUTPUT
  ```

- Apply edge enhance:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:5:1:1:1:0:128:128:128, hwdownload" OUTPUT
  ```

- Apply edge detect:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:5:5:5:1:0:128:128:128, hwdownload" OUTPUT
  ```

- Apply laplacian edge detector which includes diagonals:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:5:5:5:1:0:128:128:0, hwdownload" OUTPUT
  ```

- Apply emboss:

  ``` text
  -i INPUT -vf "hwupload, convolution_opencl=-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2, hwdownload" OUTPUT
  ```
