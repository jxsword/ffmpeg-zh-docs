# chromakey_cuda

CUDA accelerated YUV colorspace color/chroma keying.

This filter works like normal chromakey filter but operates on CUDA frames. for more details and parameters see [chromakey](chromakey.md#chromakey).

## Examples

- Make all the green pixels in the input video transparent and use it as an overlay for another video:

  ``` text
  ./ffmpeg \
      -hwaccel cuda -hwaccel_output_format cuda -i input_green.mp4  \
      -hwaccel cuda -hwaccel_output_format cuda -i base_video.mp4 \
      -init_hw_device cuda \
      -filter_complex \
      " \
          [0:v]chromakey_cuda=0x25302D:0.1:0.12:1[overlay_video]; \
          [1:v]scale_cuda=format=yuv420p[base]; \
          [base][overlay_video]overlay_cuda" \
      -an -sn -c:v h264_nvenc -cq 20 output.mp4
  ```

- Process two software sources, explicitly uploading the frames:

  ``` text
  ./ffmpeg -init_hw_device cuda=cuda -filter_hw_device cuda \
      -f lavfi -i color=size=800x600:color=white,format=yuv420p \
      -f lavfi -i yuvtestsrc=size=200x200,format=yuv420p \
      -filter_complex \
      " \
          [0]hwupload[under]; \
          [1]hwupload,chromakey_cuda=green:0.1:0.12[over]; \
          [under][over]overlay_cuda" \
      -c:v hevc_nvenc -cq 18 -preset slow output.mp4
  ```
