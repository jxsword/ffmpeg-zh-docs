# apad

Pad the end of an audio stream with silence.

This can be used together with `ffmpeg` `-shortest` to extend audio streams to the same length as the video stream.

A description of the accepted options follows.

- **`packet_size`** Set silence packet size. Default value is 4096.

- **`pad_len`** Set the number of samples of silence to add to the end. After the value is reached, the stream is terminated. This option is mutually exclusive with `whole_len`.

- **`whole_len`** Set the minimum total number of samples in the output audio stream. If the value is longer than the input audio length, silence is added to the end, until the value is reached. This option is mutually exclusive with `pad_len`.

- **`pad_dur`** Specify the duration of samples of silence to add. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. Used only if set to non-negative value.

- **`whole_dur`** Specify the minimum total duration in the output audio stream. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. Used only if set to non-negative value. If the value is longer than the input audio length, silence is added to the end, until the value is reached. This option is mutually exclusive with `pad_dur`

If neither the `pad_len` nor the `whole_len` nor `pad_dur` nor `whole_dur` option is set, the filter will add silence to the end of the input stream indefinitely.

Note that for ffmpeg 4.4 and earlier a zero `pad_dur` or `whole_dur` also caused the filter to add silence indefinitely.

## Examples

- Add 1024 samples of silence to the end of the input:

  ``` text
  apad=pad_len=1024
  ```

- Make sure the audio output will contain at least 10000 samples, pad the input with silence if required:

  ``` text
  apad=whole_len=10000
  ```

- Use `ffmpeg` to pad the audio input with silence, so that the video stream will always result the shortest and will be converted until the end in the output file when using the `shortest` option:

  ``` text
  ffmpeg -i VIDEO -i AUDIO -filter_complex "[1:0]apad" -shortest OUTPUT
  ```
