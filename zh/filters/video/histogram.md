# histogram

Compute and draw a color distribution histogram for the input video.

The computed histogram is a representation of the color component distribution in an image.

Standard histogram displays the color components distribution in an image. Displays color graph for each color component. Shows distribution of the Y, U, V, A or R, G, B components, depending on input format, in the current frame. Below each graph a color component scale meter is shown.

The filter accepts the following options:

- **`level_height`** Set height of level. Default value is `200`. Allowed range is \[50, 2048\].

- **`scale_height`** Set height of color scale. Default value is `12`. Allowed range is \[0, 40\].

- **`display_mode`** Set display mode. It accepts the following values:

  - **`stack`** Per color component graphs are placed below each other.

  - **`parade`** Per color component graphs are placed side by side.

  - **`overlay`** Presents information identical to that in the `parade`, except that the graphs representing color components are superimposed directly over one another.

  Default is `stack`.

- **`levels_mode`** Set mode. Can be either `linear`, or `logarithmic`. Default is `linear`.

- **`components`** Set what color components to display. Default is `7`.

- **`fgopacity`** Set foreground opacity. Default is `0.7`.

- **`bgopacity`** Set background opacity. Default is `0.5`.

- **`colors_mode`** Set colors mode. It accepts the following values:

  - **`whiteonblack`**

  - **`blackonwhite`**

  - **`whiteongray`**

  - **`blackongray`**

  - **`coloronblack`**

  - **`coloronwhite`**

  - **`colorongray`**

  - **`blackoncolor`**

  - **`whiteoncolor`**

  - **`grayoncolor`**

  Default is `whiteonblack`.

## Examples

- Calculate and draw histogram:

  ``` text
  ffplay -i input -vf histogram
  ```
