# field

Extract a single field from an interlaced image using stride arithmetic to avoid wasting CPU time. The output frames are marked as non-interlaced.

The filter accepts the following options:

- **`type`** Specify whether to extract the top (if the value is `0` or `top`) or the bottom field (if the value is `1` or `bottom`).
