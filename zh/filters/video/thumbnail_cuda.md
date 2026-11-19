# thumbnail_cuda

Select the most representative frame in a given sequence of consecutive frames using CUDA.

The filter accepts the following options:

- **`n`** Set the frames batch size to analyze; in a set of \<n\> frames, the filter will pick one of them, and then handle the next batch of \<n\> frames until the end. Default is `100`.

Since the filter keeps track of the whole frames sequence, a bigger \<n\> value will result in a higher memory usage, so a high value is not recommended.

## Example

- Thumbnails are extracted from every \<n\>=150-frame batch, selecting one per batch. Chosen frames are then scaled with [scale_cuda](../overview.md#examples).

  ``` text
  ./ffmpeg  -hwaccel cuda -hwaccel_output_format cuda  -i ./input.mp4 -vf "thumbnail_cuda=150,scale_cuda=1920:1080,hwdownload,format=nv12" ./output/out%03d.png
  ```
