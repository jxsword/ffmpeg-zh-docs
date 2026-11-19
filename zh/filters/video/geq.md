# geq

Apply generic equation to each pixel.

The filter accepts the following options:

| Term            | Description                          |
|-----------------|--------------------------------------|
| `lum_expr, lum` | Set the luma expression.             |
| `cb_expr, cb`   | Set the chrominance blue expression. |
| `cr_expr, cr`   | Set the chrominance red expression.  |
| `alpha_expr, a` | Set the alpha expression.            |
| `red_expr, r`   | Set the red expression.              |
| `green_expr, g` | Set the green expression.            |
| `blue_expr, b`  | Set the blue expression.             |

The colorspace is selected according to the specified options. If one of the `lum_expr`, `cb_expr`, or `cr_expr` options is specified, the filter will automatically select a YCbCr colorspace. If one of the `red_expr`, `green_expr`, or `blue_expr` options is specified, it will select an RGB colorspace.

If one of the chrominance expression is not defined, it falls back on the other one. If no alpha expression is specified it will evaluate to opaque value. If none of chrominance expressions are specified, they will evaluate to the luma expression.

The expressions can use the following variables and functions:

- **`N`** The sequential number of the filtered frame, starting from `0`.

- **`X`**

- **`Y`** The coordinates of the current sample.

- **`W`**

- **`H`** The width and height of the image.

- **`SW`**

- **`SH`** Width and height scale depending on the currently filtered plane. It is the ratio between the corresponding luma plane number of pixels and the current plane ones. E.g. for YUV4:2:0 the values are `1,1` for the luma plane, and `0.5,0.5` for chroma planes.

- **`T`** Time of the current frame, expressed in seconds.

- **`p(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the current plane.

- **`lum(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the luma plane.

- **`cb(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the blue-difference chroma plane. Return 0 if there is no such plane.

- **`cr(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the red-difference chroma plane. Return 0 if there is no such plane.

- **`r(x, y)`**

- **`g(x, y)`**

- **`b(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the red/green/blue component. Return 0 if there is no such component.

- **`alpha(x, y)`** Return the value of the pixel at location (\<x\>,\<y\>) of the alpha plane. Return 0 if there is no such plane.

- **`psum(x,y), lumsum(x, y), cbsum(x,y), crsum(x,y), rsum(x,y), gsum(x,y), bsum(x,y), alphasum(x,y)`** Sum of sample values in the rectangle from (0,0) to (x,y), this allows obtaining sums of samples within a rectangle. See the functions without the sum postfix.

- **`interpolation`** Set one of interpolation methods:

  - **`nearest, n`**

  - **`bilinear, b`**

  Default is bilinear.

For functions, if \<x\> and \<y\> are outside the area, the value will be automatically clipped to the closer edge.

Please note that this filter can use multiple threads in which case each slice will have its own expression state. If you want to use only a single expression state because your expressions depend on previous state then you should limit the number of filter threads to 1.

## Examples

- Flip the image horizontally:

  ``` text
  geq=p(W-X\,Y)
  ```

- Generate a bidimensional sine wave, with angle `PI/3` and a wavelength of 100 pixels:

  ``` text
  geq=128 + 100*sin(2*(PI/100)*(cos(PI/3)*(X-50*T) + sin(PI/3)*Y)):128:128
  ```

- Generate a fancy enigmatic moving light:

  ``` text
  nullsrc=s=256x256,geq=random(1)/hypot(X-cos(N*0.07)*W/2-W/2\,Y-sin(N*0.09)*H/2-H/2)^2*1000000*sin(N*0.02):128:128
  ```

- Generate a quick emboss effect:

  ``` text
  format=gray,geq=lum_expr='(p(X,Y)+(256-p(X-4,Y-4)))/2'
  ```

- Modify RGB components depending on pixel position:

  ``` text
  geq=r='X/W*r(X,Y)':g='(1-X/W)*g(X,Y)':b='(H-Y)/H*b(X,Y)'
  ```

- Create a radial gradient that is the same size as the input (also see the [vignette](vignette.md#vignette) filter):

  ``` text
  geq=lum=255*gauss((X/W-0.5)*3)*gauss((Y/H-0.5)*3)/gauss(0)/gauss(0),format=gray
  ```
