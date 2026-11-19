# vidstabdetect

Analyze video stabilization/deshaking. Perform pass 1 of 2, see [vidstabtransform](vidstabtransform.md#vidstabtransform) for pass 2.

This filter generates a file with relative translation and rotation transform information about subsequent frames, which is then used by the [vidstabtransform](vidstabtransform.md#vidstabtransform) filter.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libvidstab`.

This filter accepts the following options:

- **`result`** Set the path to the file used to write the transforms information. Default value is `transforms.trf`.

- **`shakiness`** Set how shaky the video is and how quick the camera is. It accepts an integer in the range 1-10, a value of 1 means little shakiness, a value of 10 means strong shakiness. Default value is 5.

- **`accuracy`** Set the accuracy of the detection process. It must be a value in the range 1-15. A value of 1 means low accuracy, a value of 15 means high accuracy. Default value is 15.

- **`stepsize`** Set stepsize of the search process. The region around minimum is scanned with 1 pixel resolution. Default value is 6.

- **`mincontrast`** Set minimum contrast. Below this value a local measurement field is discarded. Must be a floating point value in the range 0-1. Default value is 0.3.

- **`tripod`** Set reference frame number for tripod mode.

  If enabled, the motion of the frames is compared to a reference frame in the filtered stream, identified by the specified number. The idea is to compensate all movements in a more-or-less static scene and keep the camera view absolutely still.

  If set to 0, it is disabled. The frames are counted starting from 1.

- **`show`** Show fields and transforms in the resulting frames. It accepts an integer in the range 0-2. Default value is 0, which disables any visualization.

- **`fileformat`** Format for the transforms data file to be written. Acceptable values are

  - **`ascii`** Human-readable plain text

  - **`binary`** Binary format, roughly 40% smaller than `ascii`. (*default*)

## Examples

- Use default values:

  ``` text
  vidstabdetect
  ```

- Analyze strongly shaky movie and put the results in file `mytransforms.trf`:

  ``` text
  vidstabdetect=shakiness=10:accuracy=15:result="mytransforms.trf"
  ```

- Visualize the result of internal transformations in the resulting video:

  ``` text
  vidstabdetect=show=1
  ```

- Analyze a video with medium shakiness using `ffmpeg`:

  ``` text
  ffmpeg -i input -vf vidstabdetect=shakiness=5:show=1 dummy.avi
  ```
