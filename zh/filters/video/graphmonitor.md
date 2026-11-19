# graphmonitor

Show various filtergraph stats.

With this filter one can debug complete filtergraph. Especially issues with links filling with queued frames.

The filter accepts the following options:

- **`size, s`** Set video output size. Default is \<hd720\>.

- **`opacity, o`** Set video opacity. Default is \<0.9\>. Allowed range is from \<0\> to \<1\>.

- **`mode, m`** Set output mode flags.

  Available values for flags are:

  | Term           | Description                                     |
  |----------------|-------------------------------------------------|
  | `full`       | No any filtering. Default.                      |
  | `compact`    | Show only filters with queued frames.           |
  | `nozero`     | Show only filters with non-zero stats.          |
  | `noeof`      | Show only filters with non-eof stat.            |
  | `nodisabled` | Show only filters that are enabled in timeline. |

- **`flags, f`** Set flags which enable which stats are shown in video.

  Available values for flags are:

  - **`none`** All flags turned off.

  - **`all`** All flags turned on.

  - **`queue`** Display number of queued frames in each link.

  - **`frame_count_in`** Display number of frames taken from filter.

  - **`frame_count_out`** Display number of frames given out from filter.

  - **`frame_count_delta`** Display delta number of frames between above two values.

  - **`pts`** Display current filtered frame pts.

  - **`pts_delta`** Display pts delta between current and previous frame.

  - **`time`** Display current filtered frame time.

  - **`time_delta`** Display time delta between current and previous frame.

  - **`timebase`** Display time base for filter link.

  - **`format`** Display used format for filter link.

  - **`size`** Display video size or number of audio channels in case of audio used by filter link.

  - **`rate`** Display video frame rate or sample rate in case of audio used by filter link.

  - **`eof`** Display link output status.

  - **`sample_count_in`** Display number of samples taken from filter.

  - **`sample_count_out`** Display number of samples given out from filter.

  - **`sample_count_delta`** Display delta number of samples between above two values.

  - **`disabled`** Show the timeline filter status.

- **`rate, r`** Set upper limit for video rate of output stream, Default value is \<25\>. This guarantee that output video frame rate will not be higher than this value.
