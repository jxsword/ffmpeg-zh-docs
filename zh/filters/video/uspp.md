# uspp

Apply ultra slow/simple postprocessing filter that compresses and decompresses the image at several (or - in the case of `quality` level `8` - all) shifts and average the results.

The way this differs from the behavior of spp is that uspp actually encodes & decodes each case with libavcodec Snow, whereas spp uses a simplified intra only 8x8 DCT similar to MJPEG.

This filter is not available in ffmpeg versions between 5.0 and 6.0.

The filter accepts the following options:

- **`quality`** Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 0-8. If set to `0`, the filter will have no effect. A value of `8` means the higher quality. For each increment of that value the speed drops by a factor of approximately 2. Default value is `3`.

- **`qp`** Force a constant quantization parameter. If not set, the filter will use the QP from the video stream (if available).

- **`codec`** Use specified codec instead of snow.
