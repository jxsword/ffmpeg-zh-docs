# tpad

Temporarily pad video frames.

The filter accepts the following options:

- **`start`** Specify number of delay frames before input video stream. Default is 0.

- **`stop`** Specify number of padding frames after input video stream. Set to -1 to pad indefinitely. Default is 0.

- **`start_mode`** Set kind of frames added to beginning of stream. Can be either \<add\> or \<clone\>. With \<add\> frames of solid-color are added. With \<clone\> frames are clones of first frame. Default is \<add\>.

- **`stop_mode`** Set kind of frames added to end of stream. Can be either \<add\> or \<clone\>. With \<add\> frames of solid-color are added. With \<clone\> frames are clones of last frame. Default is \<add\>.

- **`start_duration, stop_duration`** Specify the duration of the start/stop delay. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. These options override \<start\> and \<stop\>. Default is 0.

- **`color`** Specify the color of the padded area. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<color\> is "black".
