# vidstabtransform

Video stabilization/deshaking: pass 2 of 2, see [vidstabdetect](vidstabdetect.md#vidstabdetect) for pass 1.

Read a file with transform information for each frame and apply/compensate them. Together with the [vidstabdetect](vidstabdetect.md#vidstabdetect) filter this can be used to deshake videos. See also <http://public.hronopik.de/vid.stab>. It is important to also use the [unsharp](unsharp.md#unsharp) filter, see below.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libvidstab`.

## Options

- **`input`** Set path to the file used to read the transforms. Default value is `transforms.trf`.

- **`smoothing`** Set the number of frames (value\*2 + 1) used for lowpass filtering the camera movements. Default value is 10.

  For example a number of 10 means that 21 frames are used (10 in the past and 10 in the future) to smoothen the motion in the video. A larger value leads to a smoother video, but limits the acceleration of the camera (pan/tilt movements). 0 is a special case where a static camera is simulated.

- **`optalgo`** Set the camera path optimization algorithm.

  Accepted values are:

  | Term      | Description                                                |
  |-----------|------------------------------------------------------------|
  | `gauss` | gaussian kernel low-pass filter on camera motion (default) |
  | `avg`   | averaging on transformations                               |

- **`maxshift`** Set maximal number of pixels to translate frames. Default value is -1, meaning no limit.

- **`maxangle`** Set maximal angle in radians (degree\*PI/180) to rotate frames. Default value is -1, meaning no limit.

- **`crop`** Specify how to deal with borders that may be visible due to movement compensation.

  Available values are:

  | Term      | Description                                          |
  |-----------|------------------------------------------------------|
  | `keep`  | keep image information from previous frame (default) |
  | `black` | fill the border black                                |

- **`invert`** Invert transforms if set to 1. Default value is 0.

- **`relative`** Consider transforms as relative to previous frame if set to 1, absolute if set to 0. Default value is 0.

- **`zoom`** Set percentage to zoom. A positive value will result in a zoom-in effect, a negative value in a zoom-out effect. Default value is 0 (no zoom).

- **`optzoom`** Set optimal zooming to avoid borders.

  Accepted values are:

  - **`0`** disabled

  - **`1`** optimal static zoom value is determined (only very strong movements will lead to visible borders) (default)

  - **`2`** optimal adaptive zoom value is determined (no borders will be visible), see `zoomspeed`

  Note that the value given at zoom is added to the one calculated here.

- **`zoomspeed`** Set percent to zoom maximally each frame (enabled when `optzoom` is set to 2). Range is from 0 to 5, default value is 0.25.

- **`interpol`** Specify type of interpolation.

  Available values are:

  | Term         | Description                         |
  |--------------|-------------------------------------|
  | `no`       | no interpolation                    |
  | `linear`   | linear only horizontal              |
  | `bilinear` | linear in both directions (default) |
  | `bicubic`  | cubic in both directions (slow)     |

- **`tripod`** Enable virtual tripod mode if set to 1, which is equivalent to `relative=0:smoothing=0`. Default value is 0.

  Use also `tripod` option of [vidstabdetect](vidstabdetect.md#vidstabdetect).

- **`debug`** Increase log verbosity if set to 1. Also the detected global motions are written to the temporary file `global_motions.trf`. Default value is 0.

## Examples

- Use `ffmpeg` for a typical stabilization with default values:

  ``` text
  ffmpeg -i inp.mpeg -vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4 inp_stabilized.mpeg
  ```

  Note the use of the [unsharp](unsharp.md#unsharp) filter which is always recommended.

- Zoom in a bit more and load transform data from a given file:

  ``` text
  vidstabtransform=zoom=5:input="mytransforms.trf"
  ```

- Smoothen the video even more:

  ``` text
  vidstabtransform=smoothing=30
  ```
