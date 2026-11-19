# kerndeint

Deinterlace input video by applying Donald Graft's adaptive kernel deinterling. Work on interlaced parts of a video to produce progressive frames.

The description of the accepted parameters follows.

- **`thresh`** Set the threshold which affects the filter's tolerance when determining if a pixel line must be processed. It must be an integer in the range \[0,255\] and defaults to 10. A value of 0 will result in applying the process on every pixels.

- **`map`** Paint pixels exceeding the threshold value to white if set to 1. Default is 0.

- **`order`** Set the fields order. Swap fields if set to 1, leave fields alone if 0. Default is 0.

- **`sharp`** Enable additional sharpening if set to 1. Default is 0.

- **`twoway`** Enable twoway sharpening if set to 1. Default is 0.

## Examples

- Apply default values:

  ``` text
  kerndeint=thresh=10:map=0:order=0:sharp=0:twoway=0
  ```

- Enable additional sharpening:

  ``` text
  kerndeint=sharp=1
  ```

- Paint processed pixels in white:

  ``` text
  kerndeint=map=1
  ```
