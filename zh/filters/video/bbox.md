# bbox

Compute the bounding box for the non-black pixels in the input frame luma plane.

This filter computes the bounding box containing all the pixels with a luma value greater than the minimum allowed value. The parameters describing the bounding box are printed on the filter log.

The filter accepts the following option:

- **`min_val`** Set the minimal luma value. Default is `16`.

## Commands

This filter supports the all above options as [commands](#commands).
