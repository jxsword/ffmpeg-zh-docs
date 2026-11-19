# sierpinski

Generate a Sierpinski carpet/triangle fractal, and randomly pan around.

This source accepts the following options:

- **`size, s`** Set frame size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is "640x480".

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`seed`** Set seed which is used for random panning.

- **`jump`** Set max jump for single pan destination. Allowed range is from 1 to 10000.

- **`type`** Set fractal type, can be default `carpet` or `triangle`.
