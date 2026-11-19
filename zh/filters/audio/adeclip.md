# adeclip

Remove clipped samples from input audio.

Samples detected as clipped are replaced by interpolated samples using autoregressive modelling.

- **`window, w`** Set window size, in milliseconds. Allowed range is from `10` to `100`. Default value is `55` milliseconds. This sets size of window which will be processed at once.

- **`overlap, o`** Set window overlap, in percentage of window size. Allowed range is from `50` to `95`. Default value is `75` percent.

- **`arorder, a`** Set autoregression order, in percentage of window size. Allowed range is from `0` to `25`. Default value is `8` percent. This option also controls quality of interpolated samples using neighbour good samples.

- **`threshold, t`** Set threshold value. Allowed range is from `1` to `100`. Default value is `10`. Higher values make clip detection less aggressive.

- **`hsize, n`** Set size of histogram used to detect clips. Allowed range is from `100` to `9999`. Default value is `1000`. Higher values make clip detection less aggressive.

- **`method, m`** Set overlap method.

  It accepts the following values:

  - **`add, a`** Select overlap-add method. Even not interpolated samples are slightly changed with this method.

  - **`save, s`** Select overlap-save method. Not interpolated samples remain unchanged.

  Default value is `a`.
