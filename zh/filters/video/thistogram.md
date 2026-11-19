# thistogram

Compute and draw a color distribution histogram for the input video across time.

Unlike [histogram](histogram.md#histogram) video filter which only shows histogram of single input frame at certain time, this filter shows also past histograms of number of frames defined by `width` option.

The computed histogram is a representation of the color component distribution in an image.

The filter accepts the following options:

- **`width, w`** Set width of single color component output. Default value is `0`. Value of `0` means width will be picked from input video. This also set number of passed histograms to keep. Allowed range is \[0, 8192\].

- **`display_mode, d`** Set display mode. It accepts the following values:

  - **`stack`** Per color component graphs are placed below each other.

  - **`parade`** Per color component graphs are placed side by side.

  - **`overlay`** Presents information identical to that in the `parade`, except that the graphs representing color components are superimposed directly over one another.

  Default is `stack`.

- **`levels_mode, m`** Set mode. Can be either `linear`, or `logarithmic`. Default is `linear`.

- **`components, c`** Set what color components to display. Default is `7`.

- **`bgopacity, b`** Set background opacity. Default is `0.9`.

- **`envelope, e`** Show envelope. Default is disabled.

- **`ecolor, ec`** Set envelope color. Default is `gold`.

- **`slide`** Set slide mode.

  Available values for slide is:

  | Term        | Description                                  |
  |-------------|----------------------------------------------|
  | `frame`   | Draw new frame when right border is reached. |
  | `replace` | Replace old columns with new ones.           |
  | `scroll`  | Scroll from right to left.                   |
  | `rscroll` | Scroll from left to right.                   |
  | `picture` | Draw single picture.                         |

  Default is `replace`.
