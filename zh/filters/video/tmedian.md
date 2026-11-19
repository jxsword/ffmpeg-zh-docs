# tmedian

Pick median pixels from several successive input video frames.

The filter accepts the following options:

- **`radius`** Set radius of median filter. Default is 1. Allowed range is from 1 to 127.

- **`planes`** Set which planes to filter. Default value is `15`, by which all planes are processed.

- **`percentile`** Set median percentile. Default value is `0.5`. Default value of `0.5` will pick always median values, while `0` will pick minimum values, and `1` maximum values.

## Commands

This filter supports all above options as [commands](#commands), excluding option `radius`.
