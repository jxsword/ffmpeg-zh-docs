# mandelbrot

Generate a Mandelbrot set fractal, and progressively zoom towards the point specified with \<start_x\> and \<start_y\>.

This source accepts the following options:

- **`end_pts`** Set the terminal pts value. Default value is 400.

- **`end_scale`** Set the terminal scale value. Must be a floating point value. Default value is 0.3.

- **`inner`** Set the inner coloring mode, that is the algorithm used to draw the Mandelbrot fractal internal region.

  It shall assume one of the following values:

  | Term | Description |
  |----|----|
  | `black` | Set black mode. |
  | `convergence` | Show time until convergence. |
  | `mincol` | Set color based on point closest to the origin of the iterations. |
  | `period` | Set period mode. |

  Default value is \<mincol\>.

- **`bailout`** Set the bailout value. Default value is 10.0.

- **`maxiter`** Set the maximum of iterations performed by the rendering algorithm. Default value is 7189.

- **`outer`** Set outer coloring mode. It shall assume one of following values:

  | Term                         | Description                          |
  |------------------------------|--------------------------------------|
  | `iteration_count`            | Set iteration count mode.            |
  | `normalized_iteration_count` | set normalized iteration count mode. |

  Default value is \<normalized_iteration_count\>.

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`size, s`** Set frame size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is "640x480".

- **`start_scale`** Set the initial scale value. Default value is 3.0.

- **`start_x`** Set the initial x position. Must be a floating point value between -100 and 100. Default value is -0.743643887037158704752191506114774.

- **`start_y`** Set the initial y position. Must be a floating point value between -100 and 100. Default value is -0.131825904205311970493132056385139.
