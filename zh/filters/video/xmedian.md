# xmedian

Pick median pixels from several input videos.

The filter accepts the following options:

- **`inputs`** Set number of inputs. Default is 3. Allowed range is from 3 to 255. If number of inputs is even number, than result will be mean value between two median values.

- **`planes`** Set which planes to filter. Default value is `15`, by which all planes are processed.

- **`percentile`** Set median percentile. Default value is `0.5`. Default value of `0.5` will pick always median values, while `0` will pick minimum values, and `1` maximum values.

## Commands

This filter supports all above options as [commands](#commands), excluding option `inputs`.
