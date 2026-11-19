# freezedetect

Detect frozen video.

This filter logs a message and sets frame metadata when it detects that the input video has no significant change in content during a specified duration. Video freeze detection calculates the mean average absolute difference of all the components of video frames and compares it to a noise floor.

The printed times and duration are expressed in seconds. The `lavfi.freezedetect.freeze_start` metadata key is set on the first frame whose timestamp equals or exceeds the detection duration and it contains the timestamp of the first frame of the freeze. The `lavfi.freezedetect.freeze_duration` and `lavfi.freezedetect.freeze_end` metadata keys are set on the first frame after the freeze.

The filter accepts the following options:

- **`noise, n`** Set noise tolerance. Can be specified in dB (in case "dB" is appended to the specified value) or as a difference ratio between 0 and 1. Default is -60dB, or 0.001.

- **`duration, d`** Set freeze duration until notification (default is 2 seconds).
