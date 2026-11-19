# cropdetect

Auto-detect the crop size.

It calculates the necessary cropping parameters and prints the recommended parameters via the logging system. The detected dimensions correspond to the non-black or video area of the input video according to \<mode\>.

It accepts the following parameters:

- **`mode`** Depending on \<mode\> crop detection is based on either the mere black value of surrounding pixels or a combination of motion vectors and edge pixels.

  - **`black`** Detect black pixels surrounding the playing video. For fine control use option \<limit\>.

  - **`mvedges`** Detect the playing video by the motion vectors inside the video and scanning for edge pixels typically forming the border of a playing video.

- **`limit`** Set higher black value threshold, which can be optionally specified from nothing (0) to everything (255 for 8-bit based formats). An intensity value greater to the set value is considered non-black. It defaults to 24. You can also specify a value between 0.0 and 1.0 which will be scaled depending on the bitdepth of the pixel format.

- **`round`** The value which the width/height should be divisible by. It defaults to 16. The offset is automatically adjusted to center the video. Use 2 to get only even dimensions (needed for 4:2:2 video). 16 is best when encoding to most video codecs.

- **`skip`** Set the number of initial frames for which evaluation is skipped. Default is 2. Range is 0 to INT_MAX.

- **`reset_count, reset`** Set the counter that determines after how many frames cropdetect will reset the previously detected largest video area and start over to detect the current optimal crop area. Default value is 0.

  This can be useful when channel logos distort the video area. 0 indicates 'never reset', and returns the largest area encountered during playback.

- **`mv_threshold`** Set motion in pixel units as threshold for motion detection. It defaults to 8.

- **`low`**

- **`high`** Set low and high threshold values used by the Canny thresholding algorithm.

  The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold.

  \<low\> and \<high\> threshold values must be chosen in the range \[0,1\], and \<low\> should be lesser or equal to \<high\>.

  Default value for \<low\> is `5/255`, and default value for \<high\> is `15/255`.

## Examples

- Find video area surrounded by black borders:

  ``` text
  ffmpeg -i file.mp4 -vf cropdetect,metadata=mode=print -f null -
  ```

- Find an embedded video area, generate motion vectors beforehand:

  ``` text
  ffmpeg -i file.mp4 -vf mestimate,cropdetect=mode=mvedges,metadata=mode=print -f null -
  ```

- Find an embedded video area, use motion vectors from decoder:

  ``` text
  ffmpeg -flags2 +export_mvs -i file.mp4 -vf cropdetect=mode=mvedges,metadata=mode=print -f null -
  ```

## Commands

This filter supports the following commands:

- **`limit`** The command accepts the same syntax of the corresponding option. If the specified expression is not valid, it is kept at its current value.
