# dilation

Apply dilation effect to the video.

This filter replaces the pixel by the local(3x3) maximum.

It accepts the following options:

- **`threshold0`**

- **`threshold1`**

- **`threshold2`**

- **`threshold3`** Limit the maximum change for each plane, default is 65535. If 0, plane will remain unchanged.

- **`coordinates`** Flag which specifies the pixel to refer to. Default is 255 i.e. all eight pixels are used.

  Flags to local 3x3 coordinates maps like this:

  1 2 3 4 5 6 7 8

## Commands

This filter supports the all above options as [commands](#commands).
