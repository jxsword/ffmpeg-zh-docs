# premultiply_dynamic

Dynamically premultiply or unpremultiply the input video stream as needed, to match the requirements of the downstream filter graph. This is roughly equivalent to either `premultiply:inplace=yes` or `unpremultiply:inplace=yes`, or otherwise a noop.

The filter accepts the following option:

- **`planes`** Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.
