# delogo

Suppress a TV station logo by a simple interpolation of the surrounding pixels. Just set a rectangle covering the logo and watch it disappear (and sometimes something even uglier appear - your mileage may vary).

It accepts the following parameters:

- **`x`**

- **`y`** Specify the top left corner coordinates of the logo. They must be specified.

- **`w`**

- **`h`** Specify the width and height of the logo to clear. They must be specified.

- **`show`** When set to 1, a green rectangle is drawn on the screen to simplify finding the right \<x\>, \<y\>, \<w\>, and \<h\> parameters. The default value is 0.

  The rectangle is drawn on the outermost pixels which will be (partly) replaced with interpolated values. The values of the next pixels immediately outside this rectangle in each direction will be used to compute the interpolated pixel values inside the rectangle.

## Examples

- Set a rectangle covering the area with top left corner coordinates 0,0 and size 100x77:

  ``` text
  delogo=x=0:y=0:w=100:h=77
  ```
