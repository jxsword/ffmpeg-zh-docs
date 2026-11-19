# silencedetect

Detect silence in an audio stream.

This filter logs a message when it detects that the input audio volume is less or equal to a noise tolerance value for a duration greater or equal to the minimum detected noise duration.

The printed times and duration are expressed in seconds. The `lavfi.silence_start` or `lavfi.silence_start.X` metadata key is set on the first frame whose timestamp equals or exceeds the detection duration and it contains the timestamp of the first frame of the silence.

The `lavfi.silence_duration` or `lavfi.silence_duration.X` and `lavfi.silence_end` or `lavfi.silence_end.X` metadata keys are set on the first frame after the silence. If `mono` is enabled, and each channel is evaluated separately, the `.X` suffixed keys are used, and `X` corresponds to the channel number.

The filter accepts the following options:

- **`noise, n`** Set noise tolerance. Can be specified in dB (in case "dB" is appended to the specified value) or amplitude ratio. Default is -60dB, or 0.001.

- **`duration, d`** Set silence duration until notification (default is 2 seconds). See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

- **`mono, m`** Process each channel separately, instead of combined. By default is disabled.

## Examples

- Detect 5 seconds of silence with -50dB noise tolerance:

  ``` text
  silencedetect=n=-50dB:d=5
  ```

- Complete example with `ffmpeg` to detect silence with 0.0001 noise tolerance in `silence.mp3`:

  ``` text
  ffmpeg -i silence.mp3 -af silencedetect=noise=0.0001 -f null -
  ```
