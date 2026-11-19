# edgedetect

Detect and draw edges. The filter uses the Canny Edge Detection algorithm.

The filter accepts the following options:

- **`low`**

- **`high`** Set low and high threshold values used by the Canny thresholding algorithm.

  The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold.

  \<low\> and \<high\> threshold values must be chosen in the range \[0,1\], and \<low\> should be lesser or equal to \<high\>.

  Default value for \<low\> is `20/255`, and default value for \<high\> is `50/255`.

- **`mode`** Define the drawing mode.

  | Term         | Description                                       |
  |--------------|---------------------------------------------------|
  | `wires`    | Draw white/gray wires on black background.        |
  | `colormix` | Mix the colors to create a paint/cartoon effect.  |
  | `canny`    | Apply Canny edge detector on all selected planes. |

  Default value is \<wires\>.

- **`planes`** Select planes for filtering. By default all available planes are filtered.

## Examples

- Standard edge detection with custom values for the hysteresis thresholding:

  ``` text
  edgedetect=low=0.1:high=0.4
  ```

- Painting effect without thresholding:

  ``` text
  edgedetect=mode=colormix:high=0
  ```
