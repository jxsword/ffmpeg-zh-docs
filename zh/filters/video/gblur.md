# gblur

Apply Gaussian blur filter.

The filter accepts the following options:

- **`sigma`** Set horizontal sigma, standard deviation of Gaussian blur. Default is `0.5`.

- **`steps`** Set number of steps for Gaussian approximation. Default is `1`.

- **`planes`** Set which planes to filter. By default all planes are filtered.

- **`sigmaV`** Set vertical sigma, if negative it will be same as `sigma`. Default is `-1`.

## Commands

This filter supports same commands as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
