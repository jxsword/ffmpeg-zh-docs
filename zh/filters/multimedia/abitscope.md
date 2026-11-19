# abitscope

Convert input audio to a video output, displaying the audio bit scope.

The filter accepts the following options:

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `1024x256`.

- **`colors`** Specify list of colors separated by space or by '\|' which will be used to draw channels. Unrecognized or missing colors will be replaced by white color.

- **`mode, m`** Set output mode. Can be `bars` or `trace`. Default is `bars`.
