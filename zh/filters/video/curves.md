# curves

Apply color adjustments using curves.

This filter is similar to the Adobe Photoshop and GIMP curves tools. Each component (red, green and blue) has its values defined by \<N\> key points tied from each other using a smooth curve. The x-axis represents the pixel values from the input frame, and the y-axis the new pixel values to be set for the output frame.

By default, a component curve is defined by the two points \<(0;0)\> and \<(1;1)\>. This creates a straight line where each original pixel value is "adjusted" to its own value, which means no change to the image.

The filter allows you to redefine these two points and add some more. A new curve will be defined to pass smoothly through all these new coordinates. The new defined points need to be strictly increasing over the x-axis, and their \<x\> and \<y\> values must be in the \<\[0;1\]\> interval. The curve is formed by using a natural or monotonic cubic spline interpolation, depending on the \<interp\> option (default: `natural`). The `natural` spline produces a smoother curve in general while the monotonic (`pchip`) spline guarantees the transitions between the specified points to be monotonic. If the computed curves happened to go outside the vector spaces, the values will be clipped accordingly.

The filter accepts the following options:

- **`preset`** Select one of the available color presets. This option can be used in addition to the `r`, `g`, `b` parameters; in this case, the later options takes priority on the preset values. Available presets are:

  - **`none`**

  - **`color_negative`**

  - **`cross_process`**

  - **`darker`**

  - **`increase_contrast`**

  - **`lighter`**

  - **`linear_contrast`**

  - **`medium_contrast`**

  - **`negative`**

  - **`strong_contrast`**

  - **`vintage`**

  Default is `none`.

- **`master, m`** Set the master key points. These points will define a second pass mapping. It is sometimes called a "luminance" or "value" mapping. It can be used with `r`, `g`, `b` or `all` since it acts like a post-processing LUT.

- **`red, r`** Set the key points for the red component.

- **`green, g`** Set the key points for the green component.

- **`blue, b`** Set the key points for the blue component.

- **`all`** Set the key points for all components (not including master). Can be used in addition to the other key points component options. In this case, the unset component(s) will fallback on this `all` setting.

- **`psfile`** Specify a Photoshop curves file (`.acv`) to import the settings from.

- **`plot`** Save Gnuplot script of the curves in specified file.

- **`interp`** Specify the kind of interpolation. Available algorithms are:

  - **`natural`** Natural cubic spline using a piece-wise cubic polynomial that is twice continuously differentiable.

  - **`pchip`** Monotonic cubic spline using a piecewise cubic Hermite interpolating polynomial (PCHIP).

To avoid some filtergraph syntax conflicts, each key points list need to be defined using the following syntax: `x0/y0 x1/y1 x2/y2 ...`.

## Commands

This filter supports same [commands](#commands) as options.

## Examples

- Increase slightly the middle level of blue:

  ``` text
  curves=blue='0/0 0.5/0.58 1/1'
  ```

- Vintage effect:

  ``` text
  curves=r='0/0.11 .42/.51 1/0.95':g='0/0 0.50/0.48 1/1':b='0/0.22 .49/.44 1/0.8'
  ```

  Here we obtain the following coordinates for each components:

  - **\<red\>** `(0;0.11) (0.42;0.51) (1;0.95)`

  - **\<green\>** `(0;0) (0.50;0.48) (1;1)`

  - **\<blue\>** `(0;0.22) (0.49;0.44) (1;0.80)`

- The previous example can also be achieved with the associated built-in preset:

  ``` text
  curves=preset=vintage
  ```

- Or simply:

  ``` text
  curves=vintage
  ```

- Use a Photoshop preset and redefine the points of the green component:

  ``` text
  curves=psfile='MyCurvesPresets/purple.acv':green='0/0 0.45/0.53 1/1'
  ```

- Check out the curves of the `cross_process` profile using `ffmpeg` and `gnuplot`:

  ``` text
  ffmpeg -f lavfi -i color -vf curves=cross_process:plot=/tmp/curves.plt -frames:v 1 -f null -
  gnuplot -p /tmp/curves.plt
  ```
