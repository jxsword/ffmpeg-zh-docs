# blackframe

Detect frames that are (almost) completely black. Can be useful to detect chapter transitions or commercials. Output lines consist of the frame number of the detected frame, the percentage of blackness, the position in the file if known or -1 and the timestamp in seconds.

In order to display the output lines, you need to set the loglevel at least to the AV_LOG_INFO value.

This filter exports frame metadata `lavfi.blackframe.pblack`. The value represents the percentage of pixels in the picture that are below the threshold value.

It accepts the following parameters:

- **`amount`** The percentage of the pixels that have to be below the threshold; it defaults to `98`.

- **`threshold, thresh`** The threshold below which a pixel value is considered black; it defaults to `32`.
