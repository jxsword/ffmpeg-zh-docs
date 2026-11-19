# datascope

Video data analysis filter.

This filter shows hexadecimal pixel values of part of video.

The filter accepts the following options:

- **`size, s`** Set output video size.

- **`x`** Set x offset from where to pick pixels.

- **`y`** Set y offset from where to pick pixels.

- **`mode`** Set scope mode, can be one of the following:

  - **`mono`** Draw hexadecimal pixel values with white color on black background.

  - **`color`** Draw hexadecimal pixel values with input video pixel color on black background.

  - **`color2`** Draw hexadecimal pixel values on color background picked from input video, the text color is picked in such way so its always visible.

- **`axis`** Draw rows and columns numbers on left and top of video.

- **`opacity`** Set background opacity.

- **`format`** Set display number format. Can be `hex`, or `dec`. Default is `hex`.

- **`components`** Set pixel components to display. By default all pixel components are displayed.

## Commands

This filter supports same [commands](#commands) as options excluding `size` option.
