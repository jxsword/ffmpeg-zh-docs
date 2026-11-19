# vpp_amf

Scale (resize) and convert colorspace, transfer characteristics or color primaries for the input video, using AMD Advanced Media Framework library for hardware acceleration. Setting the output width and height works in the same way as for the [scale](scale.md#scale) filter.

The filter accepts the following options:

- **`w`**

- **`h`** Set the output video dimension expression. Default value is the input dimension.

  Allows for the same expressions as the [scale](scale.md#scale) filter.

- **`scale_type`** Sets the algorithm used for scaling:

  - **\<bilinear\>** Bilinear

    This is the default.

  - **\<bicubic\>** Bicubic

- **`format`** Controls the output pixel format. By default, or if none is specified, the input pixel format is used.

- **`force_original_aspect_ratio`**

- **`force_divisible_by`** Work the same as the identical [scale](scale.md#scale) filter options.

- **`reset_sar`** Works the same as the identical [scale](scale.md#scale) filter option.

- **`in_color_range`** Override input color range.

- **`out_color_range`** Specify output color range.

  The accepted values for in_trc and out_trc are:

  | Term       | Description                                  |
  |------------|----------------------------------------------|
  | `studio` | Studio (or restricted, or MPEG) color range. |
  | `full`   | Full (or JPEG) color range.                  |

- **`color_profile`** Specify all color properties at once.

  The accepted values are:

  | Term       | Description |
  |------------|-------------|
  | `bt601`  | BT.601      |
  | `bt709`  | BT.709      |
  | `bt2020` | BT.2020     |

- **`in_trc`** Override input transfer characteristics.

- **`out_trc`** Specify output transfer characteristics.

  The accepted values for in_trc and out_trc are:

  | Term             | Description                 |
  |------------------|-----------------------------|
  | `bt709`        | BT.709                      |
  | `gamma22`      | Constant gamma of 2.2       |
  | `gamma28`      | Constant gamma of 2.8       |
  | `smpte170m`    | SMPTE-170M                  |
  | `smpte240m`    | SMPTE-240M                  |
  | `linear`       | Linear                      |
  | `log`          | LOG                         |
  | `log-sqrt`     | LOG_SQRT                    |
  | `iec61966-2-4` | iec61966-2-4                |
  | `bt1361-ecg`   | BT1361_ECG                  |
  | `iec61966-2-1` | iec61966-2-1                |
  | `bt2020-10`    | BT.2020 for 10-bits content |
  | `bt2020-12`    | BT.2020 for 12-bits content |
  | `smpte2084`    | SMPTE2084                   |
  | `smpte428`     | SMPTE428                    |
  | `arib-std-b67` | ARIB_STD_B67                |

- **`in_primaries`** Override input color primaries.

- **`out_primaries`** Specify output color primaries.

  The accepted values for in_primaries and out_primaries are:

  | Term          | Description                |
  |---------------|----------------------------|
  | `bt709`     | BT.709                     |
  | `bt470m`    | BT.470M                    |
  | `bt470bg`   | BT.470BG or BT.601-6 625   |
  | `smpte170m` | SMPTE-170M or BT.601-6 525 |
  | `smpte240m` | SMPTE-240M                 |
  | `film`      | film                       |
  | `bt2020`    | BT.2020                    |
  | `smpte428`  | SMPTE-428                  |
  | `smpte431`  | SMPTE-431                  |
  | `smpte432`  | SMPTE-432                  |
  | `jedec-p22` | JEDEC P22 phosphors        |

## Examples

- Scale input to 720p, keeping aspect ratio and ensuring the output is yuv420p.

  ``` text
  vpp_amf=-2:720:format=yuv420p
  ```

- Upscale to 4K and change color profile to bt2020.

  ``` text
  vpp_amf=4096:2160:color_profile=bt2020
  ```

- Override input primaries and input transfer characteristics, change both to bt709.

  ``` text
  vpp_amf=color_profile=bt2020:in_trc=smpte2084:in_primaries=bt2020:out_trc=bt709:out_primaries=bt709
  ```
