# lut1d

Apply a 1D LUT to an input video.

The filter accepts the following options:

- **`file`** Set the 1D LUT file name.

  Currently supported formats:

  | Term     | Description |
  |----------|-------------|
  | `cube` | Iridas      |
  | `csp`  | cineSpace   |

- **`interp`** Select interpolation mode.

  Available values are:

  | Term        | Description                                        |
  |-------------|----------------------------------------------------|
  | `nearest` | Use values from the nearest defined point.         |
  | `linear`  | Interpolate values using the linear interpolation. |
  | `cosine`  | Interpolate values using the cosine interpolation. |
  | `cubic`   | Interpolate values using the cubic interpolation.  |
  | `spline`  | Interpolate values using the spline interpolation. |

## Commands

This filter supports the all above options as [commands](#commands).
