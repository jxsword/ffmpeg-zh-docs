# swaprect

Swap two rectangular objects in video.

This filter accepts the following options:

- **`w`** Set object width.

- **`h`** Set object height.

- **`x1`** Set 1st rect x coordinate.

- **`y1`** Set 1st rect y coordinate.

- **`x2`** Set 2nd rect x coordinate.

- **`y2`** Set 2nd rect y coordinate.

  All expressions are evaluated once for each frame.

The all options are expressions containing the following constants:

- **`w`**

- **`h`** The input width and height.

- **`a`** same as \<w\> / \<h\>

- **`sar`** input sample aspect ratio

- **`dar`** input display aspect ratio, it is the same as (\<w\> / \<h\>) \* \<sar\>

- **`n`** The number of the input frame, starting from 0.

- **`t`** The timestamp expressed in seconds. It's NAN if the input timestamp is unknown.

- **`pos`** the position in the file of the input frame, NAN if unknown; deprecated, do not use

## Commands

This filter supports the all above options as [commands](#commands).
