# inflate

Apply inflate effect to the video.

This filter replaces the pixel by the local(3x3) average by taking into account only values higher than the pixel.

It accepts the following options:

- **`threshold0`**

- **`threshold1`**

- **`threshold2`**

- **`threshold3`** Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

## Commands

This filter supports the all above options as [commands](#commands).
