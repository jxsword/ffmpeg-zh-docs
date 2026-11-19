# atrim

Trim the input so that the output contains one continuous subpart of the input.

It accepts the following parameters:

- **`start`** Timestamp (in seconds) of the start of the section to keep. I.e. the audio sample with the timestamp \<start\> will be the first sample in the output.

- **`end`** Specify time of the first audio sample that will be dropped, i.e. the audio sample immediately preceding the one with the timestamp \<end\> will be the last sample in the output.

- **`start_pts`** Same as \<start\>, except this option sets the start timestamp in samples instead of seconds.

- **`end_pts`** Same as \<end\>, except this option sets the end timestamp in samples instead of seconds.

- **`duration`** The maximum duration of the output in seconds.

- **`start_sample`** The number of the first sample that should be output.

- **`end_sample`** The number of the first sample that should be dropped.

`start`, `end`, and `duration` are expressed as time duration specifications; see section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils`.

Note that the first two sets of the start/end options and the `duration` option look at the frame timestamp, while the \_sample options simply count the samples that pass through the filter. So start/end_pts and start/end_sample will give different results when the timestamps are wrong, inexact or do not start at zero. Also note that this filter does not modify the timestamps. If you wish to have the output timestamps start at zero, insert the asetpts filter after the atrim filter.

If multiple start or end options are set, this filter tries to be greedy and keep all samples that match at least one of the specified constraints. To keep only the part that matches all the constraints at once, chain multiple atrim filters.

The defaults are such that all the input is kept. So it is possible to set e.g. just the end values to keep everything before the specified time.

Examples:

- Drop everything except the second minute of input:

  ``` text
  ffmpeg -i INPUT -af atrim=60:120
  ```

- Keep only the first 1000 samples:

  ``` text
  ffmpeg -i INPUT -af atrim=end_sample=1000
  ```
