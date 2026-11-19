# atadenoise

Apply an Adaptive Temporal Averaging Denoiser to the video input.

The filter accepts the following options:

- **`0a`** Set threshold A for 1st plane. Default is 0.02. Valid range is 0 to 0.3.

- **`0b`** Set threshold B for 1st plane. Default is 0.04. Valid range is 0 to 5.

- **`1a`** Set threshold A for 2nd plane. Default is 0.02. Valid range is 0 to 0.3.

- **`1b`** Set threshold B for 2nd plane. Default is 0.04. Valid range is 0 to 5.

- **`2a`** Set threshold A for 3rd plane. Default is 0.02. Valid range is 0 to 0.3.

- **`2b`** Set threshold B for 3rd plane. Default is 0.04. Valid range is 0 to 5.

  Threshold A is designed to react on abrupt changes in the input signal and threshold B is designed to react on continuous changes in the input signal.

- **`s`** Set number of frames filter will use for averaging. Default is 9. Must be odd number in range \[5, 129\].

- **`p`** Set what planes of frame filter will use for averaging. Default is all.

- **`a`** Set what variant of algorithm filter will use for averaging. Default is `p` parallel. Alternatively can be set to `s` serial.

  Parallel can be faster then serial, while other way around is never true. Parallel will abort early on first change being greater then thresholds, while serial will continue processing other side of frames if they are equal or below thresholds.

- **`0s`**

- **`1s`**

- **`2s`** Set sigma for 1st plane, 2nd plane or 3rd plane. Default is 32767. Valid range is from 0 to 32767. This options controls weight for each pixel in radius defined by size. Default value means every pixel have same weight. Setting this option to 0 effectively disables filtering.

## Commands

This filter supports same [commands](#commands) as options except option `s`. The command accepts the same syntax of the corresponding option.
