# silenceremove

Remove silence from the beginning, middle or end of the audio.

The filter accepts the following options:

- **`start_periods`** This value is used to indicate if audio should be trimmed at beginning of the audio. A value of zero indicates no silence should be trimmed from the beginning. When specifying a non-zero value, it trims audio up until it finds non-silence. Normally, when trimming silence from beginning of audio the \<start_periods\> will be `1` but it can be increased to higher values to trim all audio up to specific count of non-silence periods. Default value is `0`.

- **`start_duration`** Specify the amount of time that non-silence must be detected before it stops trimming audio. By increasing the duration, bursts of noises can be treated as silence and trimmed off. Default value is `0`.

- **`start_threshold`** This indicates what sample value should be treated as silence. For digital audio, a value of `0` may be fine but for audio recorded from analog, you may wish to increase the value to account for background noise. Can be specified in dB (in case "dB" is appended to the specified value) or amplitude ratio. Default value is `0`.

- **`start_silence`** Specify max duration of silence at beginning that will be kept after trimming. Default is 0, which is equal to trimming all samples detected as silence.

- **`start_mode`** Specify mode of detection of silence end at start of multi-channel audio. Can be \<any\> or \<all\>. Default is \<any\>. With \<any\>, any sample from any channel that is detected as non-silence will trigger end of silence trimming at start of audio stream. With \<all\>, only if every sample from every channel is detected as non-silence will trigger end of silence trimming at start of audio stream, limited usage.

- **`stop_periods`** Set the count for trimming silence from the end of audio. When specifying a positive value, it trims audio after it finds specified silence period. To remove silence from the middle of a file, specify a \<stop_periods\> that is negative. This value is then treated as a positive value and is used to indicate the effect should restart processing as specified by \<stop_periods\>, making it suitable for removing periods of silence in the middle of the audio. Default value is `0`.

- **`stop_duration`** Specify a duration of silence that must exist before audio is not copied any more. By specifying a higher duration, silence that is wanted can be left in the audio. Default value is `0`.

- **`stop_threshold`** This is the same as `start_threshold` but for trimming silence from the end of audio. Can be specified in dB (in case "dB" is appended to the specified value) or amplitude ratio. Default value is `0`.

- **`stop_silence`** Specify max duration of silence at end that will be kept after trimming. Default is 0, which is equal to trimming all samples detected as silence.

- **`stop_mode`** Specify mode of detection of silence start after start of multi-channel audio. Can be \<any\> or \<all\>. Default is \<all\>. With \<any\>, any sample from any channel that is detected as silence will trigger start of silence trimming after start of audio stream, limited usage. With \<all\>, only if every sample from every channel is detected as silence will trigger start of silence trimming after start of audio stream.

- **`detection`** Set how is silence detected.

  | Term | Description |
  |----|----|
  | `avg` | Mean of absolute values of samples in moving window. |
  | `rms` | Root squared mean of absolute values of samples in moving window. |
  | `peak` | Maximum of absolute values of samples in moving window. |
  | `median` | Median of absolute values of samples in moving window. |
  | `ptp` | Absolute of max peak to min peak difference of samples in moving window. |
  | `dev` | Standard deviation of values of samples in moving window. |

  Default value is `rms`.

- **`window`** Set duration in number of seconds used to calculate size of window in number of samples for detecting silence. Using `0` will effectively disable any windowing and use only single sample per channel for silence detection. In that case it may be needed to also set `start_silence` and/or `stop_silence` to nonzero values with also `start_duration` and/or `stop_duration` to nonzero values. Default value is `0.02`. Allowed range is from `0` to `10`.

- **`timestamp`** Set processing mode of every audio frame output timestamp.

  | Term | Description |
  |----|----|
  | `write` | Full timestamps rewrite, keep only the start time for the first output frame. |
  | `copy` | Non-dropped frames are left with same timestamp as input audio frame. |

  Defaults value is `write`.

## Examples

- The following example shows how this filter can be used to start a recording that does not contain the delay at the start which usually occurs between pressing the record button and the start of the performance:

  ``` text
  silenceremove=start_periods=1:start_duration=5:start_threshold=0.02
  ```

- Trim all silence encountered from beginning to end where there is more than 1 second of silence in audio:

  ``` text
  silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-90dB
  ```

- Trim all digital silence samples, using peak detection, from beginning to end where there is more than 0 samples of digital silence in audio and digital silence is detected in all channels at same positions in stream:

  ``` text
  silenceremove=window=0:detection=peak:stop_mode=all:start_mode=all:stop_periods=-1:stop_threshold=0
  ```

- Trim every 2nd encountered silence period from beginning to end where there is more than 1 second of silence per silence period in audio:

  ``` text
  silenceremove=stop_periods=-2:stop_duration=1:stop_threshold=-90dB
  ```

- Similar as above, but keep maximum of 0.5 seconds of silence from each trimmed period:

  ``` text
  silenceremove=stop_periods=-2:stop_duration=1:stop_threshold=-90dB:stop_silence=0.5
  ```

- Similar as above, but keep maximum of 1.5 seconds of silence from start of audio:

  ``` text
  silenceremove=stop_periods=-2:stop_duration=1:stop_threshold=-90dB:stop_silence=0.5:start_periods=1:start_duration=1:start_silence=1.5:stop_threshold=-90dB
  ```

## Commands

This filter supports some above options as [commands](#commands).
