# pseudocolor

Alter frame colors in video with pseudocolors.

This filter accepts the following options:

- **`c0`** set pixel first component expression

- **`c1`** set pixel second component expression

- **`c2`** set pixel third component expression

- **`c3`** set pixel fourth component expression, corresponds to the alpha component

- **`index, i`** set component to use as base for altering colors

- **`preset, p`** Pick one of built-in LUTs. By default is set to none.

  Available LUTs:

  - **`magma`**

  - **`inferno`**

  - **`plasma`**

  - **`viridis`**

  - **`turbo`**

  - **`cividis`**

  - **`range1`**

  - **`range2`**

  - **`shadows`**

  - **`highlights`**

  - **`solar`**

  - **`nominal`**

  - **`preferred`**

  - **`total`**

  - **`spectral`**

  - **`cool`**

  - **`heat`**

  - **`fiery`**

  - **`blues`**

  - **`green`**

  - **`helix`**

- **`opacity`** Set opacity of output colors. Allowed range is from 0 to 1. Default value is set to 1.

Each of the expression options specifies the expression to use for computing the lookup table for the corresponding pixel component values.

The expressions can contain the following constants and functions:

- **`w`**

- **`h`** The input width and height.

- **`val`** The input value for the pixel component.

- **`ymin, umin, vmin, amin`** The minimum allowed component value.

- **`ymax, umax, vmax, amax`** The maximum allowed component value.

All expressions default to "val".

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Change too high luma values to gradient:

  ``` text
  pseudocolor="'if(between(val,ymax,amax),lerp(ymin,ymax,(val-ymax)/(amax-ymax)),-1):if(between(val,ymax,amax),lerp(umax,umin,(val-ymax)/(amax-ymax)),-1):if(between(val,ymax,amax),lerp(vmin,vmax,(val-ymax)/(amax-ymax)),-1):-1'"
  ```
