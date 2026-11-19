# perspective

Correct perspective of video not recorded perpendicular to the screen.

A description of the accepted parameters follows.

- **`x0`**

- **`y0`**

- **`x1`**

- **`y1`**

- **`x2`**

- **`y2`**

- **`x3`**

- **`y3`** Set coordinates expression for top left, top right, bottom left and bottom right corners. Default values are `0:0:W:0:0:H:W:H` with which perspective will remain unchanged. If the `sense` option is set to `source`, then the specified points will be sent to the corners of the destination. If the `sense` option is set to `destination`, then the corners of the source will be sent to the specified coordinates.

  The expressions can use the following variables:

  - **`W`**

  - **`H`** the width and height of video frame.

  - **`in`** Input frame count.

  - **`on`** Output frame count.

- **`interpolation`** Set interpolation for perspective correction.

  It accepts the following values:

  - **`linear`**

  - **`cubic`**

  Default value is `linear`.

- **`sense`** Set interpretation of coordinate options.

  It accepts the following values:

  - **`0, source`** Send point in the source specified by the given coordinates to the corners of the destination.

  - **`1, destination`** Send the corners of the source to the point in the destination specified by the given coordinates.

    Default value is `source`.

- **`eval`** Set when the expressions for coordinates `x0,y0,...x3,y3` are evaluated.

  It accepts the following values:

  - **`init`** only evaluate expressions once during the filter initialization or when a command is processed

  - **`frame`** evaluate expressions for each incoming frame

  Default value is `init`.
