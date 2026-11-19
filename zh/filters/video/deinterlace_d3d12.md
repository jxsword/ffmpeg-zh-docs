# deinterlace_d3d12

Deinterlace the input video using D3D12 hardware-accelerated video processing.

This filter uses the DirectX 12 Video Processor to perform deinterlacing on GPU, supporting both simple bob and driver-defined advanced (motion-adaptive) algorithms. It requires the input to be in `d3d12` hardware pixel format.

The filter automatically queries the hardware for the required number of temporal reference frames (if needed) and manages a frame queue to supply them.

It accepts the following options:

- **`method`** The deinterlacing method. It accepts one of the following values:

  - **`default`** Select the best deinterlacing method available on the hardware. If the driver supports `custom`, that method is used; otherwise falls back to `bob`. This is the default.

  - **`bob`** Bob deinterlacing. Each field is independently scaled to full frame height. Simple and fast, but may produce visible bob artifacts on moving content.

  - **`custom`** Driver-defined advanced deinterlacing. The exact algorithm is hardware-specific and typically employs motion-adaptive techniques with temporal reference frames for higher quality.

  The default value is `default`.

- **`mode`** Specify the interlacing mode. It accepts one of the following values:

  - **`frame`** Send one frame for each frame. The output frame rate equals the input frame rate. This is the default.

  - **`field`** Send one frame for each field. The output frame rate is double the input frame rate.

  The default value is `frame`.

- **`deint`** Specify which frames to deinterlace. It accepts one of the following values:

  - **`all`** Deinterlace all frames. This is the default.

  - **`interlaced`** Only deinterlace frames marked as interlaced; progressive frames are passed through unchanged.

  The default value is `all`.

## Examples

- Deinterlace an interlaced video using software decoding and the best available hardware deinterlacing method:

  ``` text
  ffmpeg -init_hw_device d3d12va=d3d12 -filter_hw_device d3d12 -i input.ts \
         -vf "format=nv12,hwupload,deinterlace_d3d12=method=default,hwdownload,format=nv12" \
         -c:v libx264 -crf 18 output.mp4
  ```

- Deinterlace at field rate (double the frame rate) using bob method with hardware decoding (full d3d12 pipeline):

  ``` text
  ffmpeg -hwaccel d3d12va -hwaccel_output_format d3d12 -i input.ts \
         -vf "deinterlace_d3d12=method=bob:mode=field" \
         -c:v h264_d3d12va output.mp4
  ```

- Deinterlace only interlaced frames, passing progressive frames through:

  ``` text
  ffmpeg -init_hw_device d3d12va=d3d12 -filter_hw_device d3d12 -i input.ts \
         -vf "format=nv12,hwupload,deinterlace_d3d12=deint=interlaced,hwdownload,format=nv12" \
         -c:v libx264 -crf 18 output.mp4
  ```
