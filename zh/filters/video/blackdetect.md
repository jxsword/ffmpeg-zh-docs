# blackdetect, blackdetect_vulkan

Detect video intervals that are (almost) completely black. Can be useful to detect chapter transitions, commercials, or invalid recordings.

The filter outputs its detection analysis to both the log as well as frame metadata. If a black segment of at least the specified minimum duration is found, a line with the start and end timestamps as well as duration is printed to the log with level `info`. In addition, a log line with level `debug` is printed per frame showing the black amount detected for that frame.

The filter also attaches metadata to the first frame of a black segment with key `lavfi.black_start` and to the first frame after the black segment ends with key `lavfi.black_end`. The value is the frame's timestamp. This metadata is added regardless of the minimum duration specified.

The filter accepts the following options:

- **`black_min_duration, d`** Set the minimum detected black duration expressed in seconds. It must be a non-negative floating point number.

  Default value is 2.0.

- **`picture_black_ratio_th, pic_th`** Set the threshold for considering a picture "black". Express the minimum value for the ratio:

  ``` text
  nb_black_pixels / nb_pixels
  ```

  for which a picture is considered black. Default value is 0.98.

- **`pixel_black_th, pix_th`** Set the threshold for considering a pixel "black".

  The threshold expresses the maximum pixel luma value for which a pixel is considered "black". The provided value is scaled according to the following equation:

  ``` text
  absolute_threshold = luma_minimum_value + pixel_black_th * luma_range_size
  ```

  \<luma_range_size\> and \<luma_minimum_value\> depend on the input video format, the range is \[0-255\] for YUV full-range formats and \[16-235\] for YUV non full-range formats.

  Default value is 0.10.

- **`alpha`** If true, check the alpha channel instead of the luma channel. Detects frames which are (almost) transparent, instead of frames which are almost black.

  Default value is disabled.

The following example sets the maximum pixel threshold to the minimum value, and detects only black intervals of 2 or more seconds:

``` text
blackdetect=d=2:pix_th=0.00
```
