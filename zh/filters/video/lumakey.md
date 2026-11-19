# lumakey

Turn certain luma values into transparency.

The filter accepts the following options:

- **`threshold`** Set the luma which will be used as base for transparency. Default value is `0`.

- **`tolerance`** Set the range of luma values to be keyed out. Default value is `0.01`.

- **`softness`** Set the range of softness. Default value is `0`. Use this to control gradual transition from zero to full transparency.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
