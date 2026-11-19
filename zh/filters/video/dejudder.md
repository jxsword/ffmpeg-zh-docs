# dejudder

Remove judder produced by partially interlaced telecined content.

Judder can be introduced, for instance, by [pullup](pullup.md#pullup) filter. If the original source was partially telecined content then the output of `pullup,dejudder` will have a variable frame rate. May change the recorded frame rate of the container. Aside from that change, this filter will not affect constant frame rate video.

The option available in this filter is:

- **`cycle`** Specify the length of the window over which the judder repeats.

  Accepts any integer greater than 1. Useful values are:

  | Term   | Description                                                     |
  |--------|-----------------------------------------------------------------|
  | `4`  | If the original was telecined from 24 to 30 fps (Film to NTSC). |
  | `5`  | If the original was telecined from 25 to 30 fps (PAL to NTSC).  |
  | `20` | If a mixture of the two.                                        |

  The default is `4`.
