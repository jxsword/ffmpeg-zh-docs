# huesaturation

Apply hue-saturation-intensity adjustments to input video stream.

This filter operates in RGB colorspace.

This filter accepts the following options:

- **`hue`** Set the hue shift in degrees to apply. Default is 0. Allowed range is from -180 to 180.

- **`saturation`** Set the saturation shift. Default is 0. Allowed range is from -1 to 1.

- **`intensity`** Set the intensity shift. Default is 0. Allowed range is from -1 to 1.

- **`colors`** Set which primary and complementary colors are going to be adjusted. This options is set by providing one or multiple values. This can select multiple colors at once. By default all colors are selected.

  | Term  | Description        |
  |-------|--------------------|
  | `r` | Adjust reds.       |
  | `y` | Adjust yellows.    |
  | `g` | Adjust greens.     |
  | `c` | Adjust cyans.      |
  | `b` | Adjust blues.      |
  | `m` | Adjust magentas.   |
  | `a` | Adjust all colors. |

- **`strength`** Set strength of filtering. Allowed range is from 0 to 100. Default value is 1.

- **`rw, gw, bw`** Set weight for each RGB component. Allowed range is from 0 to 1. By default is set to 0.333, 0.334, 0.333. Those options are used in saturation and lightess processing.

- **`lightness`** Set preserving lightness, by default is disabled. Adjusting hues can change lightness from original RGB triplet, with this option enabled lightness is kept at same value.
