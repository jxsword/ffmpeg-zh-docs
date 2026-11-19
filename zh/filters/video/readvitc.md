# readvitc

Read vertical interval timecode (VITC) information from the top lines of a video frame.

The filter adds frame metadata key `lavfi.readvitc.tc_str` with the timecode value, if a valid timecode has been detected. Further metadata key `lavfi.readvitc.found` is set to 0/1 depending on whether timecode data has been found or not.

This filter accepts the following options:

- **`scan_max`** Set the maximum number of lines to scan for VITC data. If the value is set to `-1` the full video frame is scanned. Default is `45`.

- **`thr_b`** Set the luma threshold for black. Accepts float numbers in the range \[0.0,1.0\], default value is `0.2`. The value must be equal or less than `thr_w`.

- **`thr_w`** Set the luma threshold for white. Accepts float numbers in the range \[0.0,1.0\], default value is `0.6`. The value must be equal or greater than `thr_b`.

## Examples

- Detect and draw VITC data onto the video frame; if no valid VITC is detected, draw `--:--:--:--` as a placeholder:

  ``` text
  ffmpeg -i input.avi -filter:v 'readvitc,drawtext=fontfile=FreeMono.ttf:text=%{metadata\\:lavfi.readvitc.tc_str\\:--\\\\\\:--\\\\\\:--\\\\\\:--}:x=(w-tw)/2:y=400-ascent'
  ```
