# gblur_vulkan

Apply Gaussian blur filter on Vulkan frames.

The filter accepts the following options:

- **`sigma`** Set horizontal sigma, standard deviation of Gaussian blur. Default is `0.5`.

- **`sigmaV`** Set vertical sigma, if negative it will be same as `sigma`. Default is `-1`.

- **`planes`** Set which planes to filter. By default all planes are filtered.

- **`size`** Set the kernel size along the horizontal axis. Default is `19`.

- **`sizeV`** Set the kernel size along the vertical axis. Default is `0`, which sets to use the same value as \<size\>.
