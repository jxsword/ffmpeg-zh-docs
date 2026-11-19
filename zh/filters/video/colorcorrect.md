# colorcorrect

Adjust color white balance selectively for blacks and whites. This filter operates in YUV colorspace.

The filter accepts the following options:

- **`rl`** Set the red shadow spot. Allowed range is from -1.0 to 1.0. Default value is 0.

- **`bl`** Set the blue shadow spot. Allowed range is from -1.0 to 1.0. Default value is 0.

- **`rh`** Set the red highlight spot. Allowed range is from -1.0 to 1.0. Default value is 0.

- **`bh`** Set the blue highlight spot. Allowed range is from -1.0 to 1.0. Default value is 0.

- **`saturation`** Set the amount of saturation. Allowed range is from -3.0 to 3.0. Default value is 1.

- **`analyze`** If set to anything other than `manual` it will analyze every frame and use derived parameters for filtering output frame.

  Possible values are:

  - **`manual`**

  - **`average`**

  - **`minmax`**

  - **`median`**

  Default value is `manual`.

## Commands

This filter supports the all above options as [commands](#commands).
