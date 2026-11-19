# lut3d

Apply a 3D LUT to an input video.

The filter accepts the following options:

- **`file`** Set the 3D LUT file name.

  Currently supported formats:

  | Term     | Description  |
  |----------|--------------|
  | `3dl`  | AfterEffects |
  | `cube` | Iridas       |
  | `dat`  | DaVinci      |
  | `m3d`  | Pandora      |
  | `csp`  | cineSpace    |

- **`interp`** Select interpolation mode.

  Available values are:

  | Term            | Description                                            |
  |-----------------|--------------------------------------------------------|
  | `nearest`     | Use values from the nearest defined point.             |
  | `trilinear`   | Interpolate values using the 8 points defining a cube. |
  | `tetrahedral` | Interpolate values using a tetrahedron.                |
  | `pyramid`     | Interpolate values using a pyramid.                    |
  | `prism`       | Interpolate values using a prism.                      |

## Commands

This filter supports the `interp` option as [commands](#commands).
