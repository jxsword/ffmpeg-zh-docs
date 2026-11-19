# pad_cuda

Add paddings to an input video stream using CUDA.

This filter is the CUDA-accelerated version of the [pad](pad.md#pad) filter. It accepts the same options and expressions and provides the same core functionality. For a detailed description of available options, please see the documentation for the [pad](pad.md#pad) filter.

## Examples

- Add a 200-pixel black border to all sides of a video frame:

  ``` text
  ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 -vf "pad_cuda=w=iw+400:h=ih+400:x=200:y=200" -c:v h264_nvenc out.mp4
  ```

- Pad the input video to a 16:9 aspect ratio, filling with the color "blue":

  ``` text
  ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 -vf "pad_cuda=w=ih*16/9/sar:h=ih:x=(ow-iw)/2:y=(oh-ih)/2:color=blue" -c:v h264_nvenc out.mp4
  ```
