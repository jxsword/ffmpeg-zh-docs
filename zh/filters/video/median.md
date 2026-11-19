# median

Pick median pixel from certain rectangle defined by radius.

This filter accepts the following options:

- **`radius`** Set horizontal radius size. Default value is `1`. Allowed range is integer from 1 to 127.

- **`planes`** Set which planes to process. Default is `15`, which is all available planes.

- **`radiusV`** Set vertical radius size. Default value is `0`. Allowed range is integer from 0 to 127. If it is 0, value will be picked from horizontal `radius` option.

- **`percentile`** Set median percentile. Default value is `0.5`. Default value of `0.5` will pick always median values, while `0` will pick minimum values, and `1` maximum values.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
