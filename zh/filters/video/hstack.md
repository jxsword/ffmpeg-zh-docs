# hstack

Stack input videos horizontally.

All streams must be of same pixel format and of same height.

Note that this filter is faster than using [overlay](overlay.md#overlay) and [pad](pad.md#pad) filter to create same output.

The filter accepts the following option:

- **`inputs`** Set number of input streams. Default is 2.

- **`shortest`** If set to 1, force the output to terminate when the shortest input terminates. Default value is 0.
