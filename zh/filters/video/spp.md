# spp

Apply a simple postprocessing filter that compresses and decompresses the image at several (or - in the case of `quality` level `6` - all) shifts and average the results.

The filter accepts the following options:

- **`quality`** Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 0-6. If set to `0`, the filter will have no effect. A value of `6` means the higher quality. For each increment of that value the speed drops by a factor of approximately 2. Default value is `3`.

- **`qp`** Force a constant quantization parameter. If not set, the filter will use the QP from the video stream (if available).

- **`mode`** Set thresholding mode. Available modes are:

  | Term | Description |
  |----|----|
  | `hard` | Set hard thresholding (default). |
  | `soft` | Set soft thresholding (better de-ringing effect, but likely blurrier). |

- **`use_bframe_qp`** Enable the use of the QP from the B-Frames if set to `1`. Using this option may cause flicker since the B-Frames have often larger QP. Default is `0` (not enabled).

## Commands

This filter supports the following commands:

- **`quality, level`** Set quality level. The value `max` can be used to set the maximum level, currently `6`.
