# maskfun

Create mask from input video.

For example it is useful to create motion masks after `tblend` filter.

This filter accepts the following options:

- **`low`** Set low threshold. Any pixel component lower or exact than this value will be set to 0.

- **`high`** Set high threshold. Any pixel component higher than this value will be set to max value allowed for current pixel format.

- **`planes`** Set planes to filter, by default all available planes are filtered.

- **`fill`** Fill all frame pixels with this value.

- **`sum`** Set max average pixel value for frame. If sum of all pixel components is higher that this average, output frame will be completely filled with value set by \<fill\> option. Typically useful for scene changes when used in combination with `tblend` filter.

## Commands

This filter supports the all above options as [commands](#commands).
