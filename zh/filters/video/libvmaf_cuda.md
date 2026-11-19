# libvmaf_cuda

This is the CUDA variant of the [libvmaf](libvmaf.md#libvmaf) filter. It only accepts CUDA frames.

It requires Netflix's vmaf library (libvmaf) as a pre-requisite. After installing the library it can be enabled using: `./configure --enable-nonfree --enable-ffnvcodec --enable-libvmaf`.

## Examples

- Basic usage showing CUVID hardware decoding and CUDA scaling with [scale_cuda](../overview.md#examples):

  ``` text
  ffmpeg \
      -hwaccel cuda -hwaccel_output_format cuda -codec:v av1_cuvid -i dis.obu \
      -hwaccel cuda -hwaccel_output_format cuda -codec:v av1_cuvid -i ref.obu \
      -filter_complex "
          [0:v]scale_cuda=format=yuv420p[dis]; \
          [1:v]scale_cuda=format=yuv420p[ref]; \
          [dis][ref]libvmaf_cuda=log_fmt=json:log_path=output.json
      " \
      -f null -
  ```
