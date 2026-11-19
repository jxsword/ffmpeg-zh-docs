# selectivecolor

Adjust cyan, magenta, yellow and black (CMYK) to certain ranges of colors (such as "reds", "yellows", "greens", "cyans", ...). The adjustment range is defined by the "purity" of the color (that is, how saturated it already is).

This filter is similar to the Adobe Photoshop Selective Color tool.

The filter accepts the following options:

- **`correction_method`** Select color correction method.

  Available values are:

  - **`absolute`** Specified adjustments are applied "as-is" (added/subtracted to original pixel component value).

  - **`relative`** Specified adjustments are relative to the original component value.

  Default is `absolute`.

- **`reds`** Adjustments for red pixels (pixels where the red component is the maximum)

- **`yellows`** Adjustments for yellow pixels (pixels where the blue component is the minimum)

- **`greens`** Adjustments for green pixels (pixels where the green component is the maximum)

- **`cyans`** Adjustments for cyan pixels (pixels where the red component is the minimum)

- **`blues`** Adjustments for blue pixels (pixels where the blue component is the maximum)

- **`magentas`** Adjustments for magenta pixels (pixels where the green component is the minimum)

- **`whites`** Adjustments for white pixels (pixels where all components are greater than 128)

- **`neutrals`** Adjustments for all pixels except pure black and pure white

- **`blacks`** Adjustments for black pixels (pixels where all components are lesser than 128)

- **`psfile`** Specify a Photoshop selective color file (`.asv`) to import the settings from.

All the adjustment settings (`reds`, `yellows`, ...) accept up to 4 space separated floating point adjustment values in the \[-1,1\] range, respectively to adjust the amount of cyan, magenta, yellow and black for the pixels of its range.

## Examples

- Increase cyan by 50% and reduce yellow by 33% in every green areas, and increase magenta by 27% in blue areas:

  ``` text
  selectivecolor=greens=.5 0 -.33 0:blues=0 .27
  ```

- Use a Photoshop selective color preset:

  ``` text
  selectivecolor=psfile=MySelectiveColorPresets/Misty.asv
  ```
