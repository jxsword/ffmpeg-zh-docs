# convolution

Apply convolution of 3x3, 5x5, 7x7 or horizontal/vertical up to 49 elements.

The filter accepts the following options:

- **`0m`**

- **`1m`**

- **`2m`**

- **`3m`** Set matrix for each plane. Matrix is sequence of 9, 25 or 49 signed integers in \<square\> mode, and from 1 to 49 odd number of signed integers in \<row\> mode.

- **`0rdiv`**

- **`1rdiv`**

- **`2rdiv`**

- **`3rdiv`** Set multiplier for calculated value for each plane. If unset or 0, it will be 1/sum of all matrix elements.

- **`0bias`**

- **`1bias`**

- **`2bias`**

- **`3bias`** Set bias for each plane. This value is added to the result of the multiplication. Useful for making the overall image brighter or darker. Default is 0.0.

- **`0mode`**

- **`1mode`**

- **`2mode`**

- **`3mode`** Set matrix mode for each plane. Can be \<square\>, \<row\> or \<column\>. Default is \<square\>.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Apply sharpen:

  ``` text
  convolution="0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0"
  ```

- Apply blur:

  ``` text
  convolution="1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1 1 1 1 1 1 1 1 1:1/9:1/9:1/9:1/9"
  ```

- Apply edge enhance:

  ``` text
  convolution="0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:0 0 0 -1 1 0 0 0 0:5:1:1:1:0:128:128:128"
  ```

- Apply edge detect:

  ``` text
  convolution="0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:0 1 0 1 -4 1 0 1 0:5:5:5:1:0:128:128:128"
  ```

- Apply laplacian edge detector which includes diagonals:

  ``` text
  convolution="1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:1 1 1 1 -8 1 1 1 1:5:5:5:1:0:128:128:0"
  ```

- Apply emboss:

  ``` text
  convolution="-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2:-2 -1 0 -1 1 1 0 1 2"
  ```
