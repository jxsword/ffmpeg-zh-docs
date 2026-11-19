# colorspace

Convert colorspace, transfer characteristics or color primaries. Input video needs to have an even size.

The filter accepts the following options:

- **`all`** Specify all color properties at once.

  The accepted values are:

  | Term            | Description  |
  |-----------------|--------------|
  | `bt470m`      | BT.470M      |
  | `bt470bg`     | BT.470BG     |
  | `bt601-6-525` | BT.601-6 525 |
  | `bt601-6-625` | BT.601-6 625 |
  | `bt709`       | BT.709       |
  | `smpte170m`   | SMPTE-170M   |
  | `smpte240m`   | SMPTE-240M   |
  | `bt2020`      | BT.2020      |

- **`space`** Specify output colorspace.

  The accepted values are:

  | Term          | Description                         |
  |---------------|-------------------------------------|
  | `bt709`     | BT.709                              |
  | `fcc`       | FCC                                 |
  | `bt470bg`   | BT.470BG or BT.601-6 625            |
  | `smpte170m` | SMPTE-170M or BT.601-6 525          |
  | `smpte240m` | SMPTE-240M                          |
  | `ycgco`     | YCgCo                               |
  | `bt2020ncl` | BT.2020 with non-constant luminance |

- **`trc`** Specify output transfer characteristics.

  The accepted values are:

  | Term             | Description                              |
  |------------------|------------------------------------------|
  | `bt709`        | BT.709                                   |
  | `bt470m`       | BT.470M                                  |
  | `bt470bg`      | BT.470BG                                 |
  | `gamma22`      | Constant gamma of 2.2                    |
  | `gamma28`      | Constant gamma of 2.8                    |
  | `smpte170m`    | SMPTE-170M, BT.601-6 625 or BT.601-6 525 |
  | `smpte240m`    | SMPTE-240M                               |
  | `srgb`         | SRGB                                     |
  | `iec61966-2-1` | iec61966-2-1                             |
  | `iec61966-2-4` | iec61966-2-4                             |
  | `xvycc`        | xvycc                                    |
  | `bt2020-10`    | BT.2020 for 10-bits content              |
  | `bt2020-12`    | BT.2020 for 12-bits content              |

- **`primaries`** Specify output color primaries.

  The accepted values are:

  | Term          | Description                |
  |---------------|----------------------------|
  | `bt709`     | BT.709                     |
  | `bt470m`    | BT.470M                    |
  | `bt470bg`   | BT.470BG or BT.601-6 625   |
  | `smpte170m` | SMPTE-170M or BT.601-6 525 |
  | `smpte240m` | SMPTE-240M                 |
  | `film`      | film                       |
  | `smpte431`  | SMPTE-431                  |
  | `smpte432`  | SMPTE-432                  |
  | `bt2020`    | BT.2020                    |
  | `jedec-p22` | JEDEC P22 phosphors        |

- **`range`** Specify output color range.

  The accepted values are:

  | Term     | Description             |
  |----------|-------------------------|
  | `tv`   | TV (restricted) range   |
  | `mpeg` | MPEG (restricted) range |
  | `pc`   | PC (full) range         |
  | `jpeg` | JPEG (full) range       |

- **`format`** Specify output color format.

  The accepted values are:

  | Term          | Description              |
  |---------------|--------------------------|
  | `yuv420p`   | YUV 4:2:0 planar 8-bits  |
  | `yuv420p10` | YUV 4:2:0 planar 10-bits |
  | `yuv420p12` | YUV 4:2:0 planar 12-bits |
  | `yuv422p`   | YUV 4:2:2 planar 8-bits  |
  | `yuv422p10` | YUV 4:2:2 planar 10-bits |
  | `yuv422p12` | YUV 4:2:2 planar 12-bits |
  | `yuv444p`   | YUV 4:4:4 planar 8-bits  |
  | `yuv444p10` | YUV 4:4:4 planar 10-bits |
  | `yuv444p12` | YUV 4:4:4 planar 12-bits |

- **`fast`** Do a fast conversion, which skips gamma/primary correction. This will take significantly less CPU, but will be mathematically incorrect. To get output compatible with that produced by the colormatrix filter, use fast=1.

- **`dither`** Specify dithering mode.

  The accepted values are:

  | Term     | Description               |
  |----------|---------------------------|
  | `none` | No dithering              |
  | `fsb`  | Floyd-Steinberg dithering |

- **`wpadapt`** Whitepoint adaptation mode.

  The accepted values are:

  | Term | Description |
  |----|----|
  | `bradford` | Bradford whitepoint adaptation |
  | `vonkries` | von Kries whitepoint adaptation |
  | `identity` | identity whitepoint adaptation (i.e. no whitepoint adaptation) |

- **`clipgamut`** Controls how to clip out-of-gamut colors that arise as a result of colorspace conversion.

  The accepted values are:

  | Term | Description |
  |----|----|
  | `none` | No clipping of out of gamut colors. |
  | `rgb` | Clips the RGB values to the \[0, 1\] range when building the gamma transfer LUTs. |

- **`iall`** Override all input properties at once. Same accepted values as [all](colorspace.md#colorspace).

- **`ispace`** Override input colorspace. Same accepted values as [space](colorspace.md#colorspace).

- **`iprimaries`** Override input color primaries. Same accepted values as [primaries](colorspace.md#colorspace).

- **`itrc`** Override input transfer characteristics. Same accepted values as [trc](colorspace.md#colorspace).

- **`irange`** Override input color range. Same accepted values as [range](colorspace.md#colorspace).

The filter converts the transfer characteristics, color space and color primaries to the specified user values. The output value, if not specified, is set to a default value based on the "all" property. If that property is also not specified, the filter will log an error. The output color range and format default to the same value as the input color range and format. The input transfer characteristics, color space, color primaries and color range should be set on the input data. If any of these are missing, the filter will log an error and no conversion will take place.

For example to convert the input to SMPTE-240M, use the command:

``` text
colorspace=smpte240m
```
