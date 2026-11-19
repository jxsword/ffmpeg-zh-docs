# maskedthreshold

Pick pixels comparing absolute difference of two video streams with fixed threshold.

If absolute difference between pixel component of first and second video stream is equal or lower than user supplied threshold than pixel component from first video stream is picked, otherwise pixel component from second video stream is picked.

This filter accepts the following options:

- **`threshold`** Set threshold used when picking pixels from absolute difference from two input video streams.

- **`planes`** Set which planes will be processed as bitmap, unprocessed planes will be copied from second stream. By default value 0xf, all planes will be processed.

- **`mode`** Set mode of filter operation. Can be `abs` or `diff`. Default is `abs`.

## Commands

This filter supports the all above options as [commands](#commands).
