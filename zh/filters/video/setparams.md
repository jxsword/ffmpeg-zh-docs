# setparams

Force frame parameter for the output video frame.

The `setparams` filter marks interlace and color range for the output frames. It does not change the input frame, but only sets the corresponding property, which affects how the frame is treated by filters/encoders.

- **`field_mode`** Available values are:

  | Term     | Description                             |
  |----------|-----------------------------------------|
  | `auto` | Keep the same field property (default). |
  | `bff`  | Mark the frame as bottom-field-first.   |
  | `tff`  | Mark the frame as top-field-first.      |
  | `prog` | Mark the frame as progressive.          |

- **`range`** Available values are:

  | Term                     | Description                                   |
  |--------------------------|-----------------------------------------------|
  | `auto`                 | Keep the same color range property (default). |
  | `unspecified, unknown` | Mark the frame as unspecified color range.    |
  | `limited, tv, mpeg`    | Mark the frame as limited range.              |
  | `full, pc, jpeg`       | Mark the frame as full range.                 |

- **`color_primaries`** Set the color primaries. Available values are:

  - **`auto`** Keep the same color primaries property (default).

  - **`bt709`**

  - **`unknown`**

  - **`bt470m`**

  - **`bt470bg`**

  - **`smpte170m`**

  - **`smpte240m`**

  - **`film`**

  - **`bt2020`**

  - **`smpte428`**

  - **`smpte431`**

  - **`smpte432`**

  - **`jedec-p22`**

- **`color_trc`** Set the color transfer. Available values are:

  - **`auto`** Keep the same color trc property (default).

  - **`bt709`**

  - **`unknown`**

  - **`bt470m`**

  - **`bt470bg`**

  - **`smpte170m`**

  - **`smpte240m`**

  - **`linear`**

  - **`log100`**

  - **`log316`**

  - **`iec61966-2-4`**

  - **`bt1361e`**

  - **`iec61966-2-1`**

  - **`bt2020-10`**

  - **`bt2020-12`**

  - **`smpte2084`**

  - **`smpte428`**

  - **`arib-std-b67`**

- **`colorspace`** Set the colorspace. Available values are:

  - **`auto`** Keep the same colorspace property (default).

  - **`gbr`**

  - **`bt709`**

  - **`unknown`**

  - **`fcc`**

  - **`bt470bg`**

  - **`smpte170m`**

  - **`smpte240m`**

  - **`ycgco`**

  - **`bt2020nc`**

  - **`bt2020c`**

  - **`smpte2085`**

  - **`chroma-derived-nc`**

  - **`chroma-derived-c`**

  - **`ictcp`**

- **`chroma_location`** Set the chroma sample location. Available values are:

  - **`auto`** Keep the same chroma location (default).

  - **`unspecified, unknown`**

  - **`left`**

  - **`center`**

  - **`topleft`**

  - **`top`**

  - **`bottomleft`**

  - **`bottom`**

- **`alpha_mode`** Set the alpha moda. Available values are:

  - **`auto`** Keep the same alpha mode (default).

  - **`unspecified, unknown`**

  - **`premultiplied`**

  - **`straight`**
