# dctdnoiz

Denoise frames using 2D DCT (frequency domain filtering).

This filter is not designed for real time.

The filter accepts the following options:

- **`sigma, s`** Set the noise sigma constant.

  This \<sigma\> defines a hard threshold of `3 * sigma`; every DCT coefficient (absolute value) below this threshold with be dropped.

  If you need a more advanced filtering, see `expr`.

  Default is `0`.

- **`overlap`** Set number overlapping pixels for each block. Since the filter can be slow, you may want to reduce this value, at the cost of a less effective filter and the risk of various artefacts.

  If the overlapping value doesn't permit processing the whole input width or height, a warning will be displayed and according borders won't be denoised.

  Default value is \<blocksize\>-1, which is the best possible setting.

- **`expr, e`** Set the coefficient factor expression.

  For each coefficient of a DCT block, this expression will be evaluated as a multiplier value for the coefficient.

  If this is option is set, the `sigma` option will be ignored.

  The absolute value of the coefficient can be accessed through the \<c\> variable.

- **`n`** Set the \<blocksize\> using the number of bits. `1<<n` defines the \<blocksize\>, which is the width and height of the processed blocks.

  The default value is \<3\> (8x8) and can be raised to \<4\> for a \<blocksize\> of 16x16. Note that changing this setting has huge consequences on the speed processing. Also, a larger block size does not necessarily means a better de-noising.

## Examples

Apply a denoise with a `sigma` of `4.5`:

``` text
dctdnoiz=4.5
```

The same operation can be achieved using the expression system:

``` text
dctdnoiz=e='gte(c, 4.5*3)'
```

Violent denoise using a block size of `16x16`:

``` text
dctdnoiz=15:n=4
```
