# pp7

Apply Postprocessing filter 7. It is variant of the [spp](spp.md#spp) filter, similar to spp = 6 with 7 point DCT, where only the center sample is used after IDCT.

The filter accepts the following options:

- **`qp`** Force a constant quantization parameter. It accepts an integer in range 0 to 63. If not set, the filter will use the QP from the video stream (if available).

- **`mode`** Set thresholding mode. Available modes are:

  | Term | Description |
  |----|----|
  | `hard` | Set hard thresholding. |
  | `soft` | Set soft thresholding (better de-ringing effect, but likely blurrier). |
  | `medium` | Set medium thresholding (good results, default). |
