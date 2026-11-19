# shear

Apply shear transform to input video.

This filter supports the following options:

- **`shx`** Shear factor in X-direction. Default value is 0. Allowed range is from -2 to 2.

- **`shy`** Shear factor in Y-direction. Default value is 0. Allowed range is from -2 to 2.

- **`fillcolor, c`** Set the color used to fill the output area not covered by the transformed video. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. If the special value "none" is selected then no background is printed (useful for example if the background is never shown).

  Default value is "black".

- **`interp`** Set interpolation type. Can be `bilinear` or `nearest`. Default is `bilinear`.

## Commands

This filter supports the all above options as [commands](#commands).
