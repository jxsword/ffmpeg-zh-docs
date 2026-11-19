# trim

Trim the input so that the output contains one continuous subpart of the input.

It accepts the following parameters:

- **`start`** Specify the time of the start of the kept section, i.e. the frame with the timestamp \<start\> will be the first frame in the output.

- **`end`** Specify the time of the first frame that will be dropped, i.e. the frame immediately preceding the one with the timestamp \<end\> will be the last frame in the output.

- **`start_pts`** This is the same as \<start\>, except this option sets the start timestamp in timebase units instead of seconds.

- **`end_pts`** This is the same as \<end\>, except this option sets the end timestamp in timebase units instead of seconds.

- **`duration`** The maximum duration of the output in seconds.

- **`start_frame`** The number of the first frame that should be passed to the output.

- **`end_frame`** The number of the first frame that should be dropped.

`start`, `end`, and `duration` are expressed as time duration specifications; see section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

Note that the first two sets of the start/end options and the `duration` option look at the frame timestamp, while the \_frame variants simply count the frames that pass through the filter. Also note that this filter does not modify the timestamps. If you wish for the output timestamps to start at zero, insert a setpts filter after the trim filter.

If multiple start or end options are set, this filter tries to be greedy and keep all the frames that match at least one of the specified constraints. To keep only the part that matches all the constraints at once, chain multiple trim filters.

The defaults are such that all the input is kept. So it is possible to set e.g. just the end values to keep everything before the specified time.

Examples:

- Drop everything except the second minute of input:

  ``` text
  ffmpeg -i INPUT -vf trim=60:120
  ```

- Keep only the first second:

  ``` text
  ffmpeg -i INPUT -vf trim=duration=1
  ```
