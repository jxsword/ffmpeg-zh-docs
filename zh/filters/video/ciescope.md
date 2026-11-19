# ciescope

Display CIE color diagram with pixels overlaid onto it.

The filter accepts the following options:

- **`system`** Set color system.

  - **`ntsc, 470m`**

  - **`ebu, 470bg`**

  - **`smpte`**

  - **`240m`**

  - **`apple`**

  - **`widergb`**

  - **`cie1931`**

  - **`rec709, hdtv`**

  - **`uhdtv, rec2020`**

  - **`dcip3`**

- **`cie`** Set CIE system.

  - **`xyy`**

  - **`ucs`**

  - **`luv`**

- **`gamuts`** Set what gamuts to draw.

  See `system` option for available values.

- **`size, s`** Set ciescope size, by default set to 512.

- **`intensity, i`** Set intensity used to map input pixel values to CIE diagram.

- **`contrast`** Set contrast used to draw tongue colors that are out of active color system gamut.

- **`corrgamma`** Correct gamma displayed on scope, by default enabled.

- **`showwhite`** Show white point on CIE diagram, by default disabled.

- **`gamma`** Set input gamma. Used only with XYZ input color space.

- **`fill`** Fill with CIE colors. By default is enabled.
