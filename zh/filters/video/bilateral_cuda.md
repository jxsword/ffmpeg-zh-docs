# bilateral_cuda

CUDA accelerated bilateral filter, an edge preserving filter. This filter is mathematically accurate thanks to the use of GPU acceleration. For best output quality, use one to one chroma subsampling, i.e. yuv444p format.

The filter accepts the following options:

- **`sigmaS`** Set sigma of gaussian function to calculate spatial weight, also called sigma space. Allowed range is 0.1 to 512. Default is 0.1.

- **`sigmaR`** Set sigma of gaussian function to calculate color range weight, also called sigma color. Allowed range is 0.1 to 512. Default is 0.1.

- **`window_size`** Set window size of the bilateral function to determine the number of neighbours to loop on. If the number entered is even, one will be added automatically. Allowed range is 1 to 255. Default is 1.

## Examples

- Apply the bilateral filter on a video.

  ``` text
  ./ffmpeg -v verbose \
  -hwaccel cuda -hwaccel_output_format cuda -i input.mp4  \
  -init_hw_device cuda \
  -filter_complex \
  " \
  [0:v]scale_cuda=format=yuv444p[scaled_video];
  [scaled_video]bilateral_cuda=window_size=9:sigmaS=3.0:sigmaR=50.0" \
  -an -sn -c:v h264_nvenc -cq 20 out.mp4
  ```
