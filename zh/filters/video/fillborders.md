# fillborders

Fill borders of the input video, without changing video stream dimensions. Sometimes video can have garbage at the four edges and you may not want to crop video input to keep size multiple of some number.

This filter accepts the following options:

- **`left`** Number of pixels to fill from left border.

- **`right`** Number of pixels to fill from right border.

- **`top`** Number of pixels to fill from top border.

- **`bottom`** Number of pixels to fill from bottom border.

- **`mode`** Set fill mode.

  It accepts the following values:

  | Term | Description |
  |----|----|
  | `smear` | fill pixels using outermost pixels |
  | `mirror` | fill pixels using mirroring (half sample symmetric) |
  | `fixed` | fill pixels with constant value |
  | `reflect` | fill pixels using reflecting (whole sample symmetric) |
  | `wrap` | fill pixels using wrapping |
  | `fade` | fade pixels to constant value |
  | `margins` | fill pixels at top and bottom with weighted averages pixels near borders |

  Default is \<smear\>.

- **`color`** Set color for pixels in fixed or fade mode. Default is \<black\>.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
