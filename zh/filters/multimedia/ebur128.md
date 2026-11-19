# ebur128

EBU R128 scanner filter. This filter takes an audio stream and analyzes its loudness level. By default, it logs a message at a frequency of 10Hz with the Momentary loudness (identified by `M`), Short-term loudness (`S`), Integrated loudness (`I`) and Loudness Range (`LRA`).

The filter can only analyze streams which have sample format is double-precision floating point. The input stream will be converted to this specification, if needed. Users may need to insert aformat and/or aresample filters after this filter to obtain the original parameters.

The filter also has a video output (see the \<video\> option) with a real time graph to observe the loudness evolution. The graphic contains the logged message mentioned above, so it is not printed anymore when this option is set, unless the verbose logging is set. The main graphing area contains the short-term loudness (3 seconds of analysis), and the gauge on the right is for the momentary loudness (400 milliseconds), but can optionally be configured to instead display short-term loudness (see \<gauge\>).

The green area marks a +/- 1LU target range around the target loudness (-23LUFS by default, unless modified through \<target\>).

More information about the Loudness Recommendation EBU R128 on <http://tech.ebu.ch/loudness>.

The filter accepts the following options:

- **`video`** Activate the video output. The audio stream is passed unchanged whether this option is set or no. The video stream will be the first output stream if activated. Default is `0`.

- **`size`** Set the video size. This option is for video only. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default and minimum resolution is `640x480`.

- **`meter`** Set the EBU scale meter. Default is `9`. Common values are `9` and `18`, respectively for EBU scale meter +9 and EBU scale meter +18. Any other integer value between this range is allowed.

- **`metadata`** Set metadata injection. If set to `1`, the audio input will be segmented into 100ms output frames, each of them containing various loudness information in metadata. All the metadata keys are prefixed with `lavfi.r128.`.

  Default is `0`.

- **`framelog`** Force the frame logging level.

  Available values are:

  | Term        | Description               |
  |-------------|---------------------------|
  | `quiet`   | logging disabled          |
  | `info`    | information logging level |
  | `verbose` | verbose logging level     |

  By default, the logging level is set to \<info\>. If the `video` or the `metadata` options are set, it switches to \<verbose\>.

- **`peak`** Set peak mode(s).

  Available modes can be cumulated (the option is a `flag` type). Possible values are:

  - **`none`** Disable any peak mode (default).

  - **`sample`** Enable sample-peak mode.

    Simple peak mode looking for the higher sample value. It logs a message for sample-peak (identified by `SPK`).

  - **`true`** Enable true-peak mode.

    If enabled, the peak lookup is done on an over-sampled version of the input stream for better peak accuracy. It logs a message for true-peak. (identified by `TPK`) and true-peak per frame (identified by `FTPK`). This mode requires a build with `libswresample`.

- **`dualmono`** Treat mono input files as "dual mono". If a mono file is intended for playback on a stereo system, its EBU R128 measurement will be perceptually incorrect. If set to `true`, this option will compensate for this effect. Multi-channel input files are not affected by this option.

- **`panlaw`** Set a specific pan law to be used for the measurement of dual mono files. This parameter is optional, and has a default value of -3.01dB.

- **`target`** Set a specific target level (in LUFS) used as relative zero in the visualization. This parameter is optional and has a default value of -23LUFS as specified by EBU R128. However, material published online may prefer a level of -16LUFS (e.g. for use with podcasts or video platforms).

- **`gauge`** Set the value displayed by the gauge. Valid values are `momentary` and s `shortterm`. By default the momentary value will be used, but in certain scenarios it may be more useful to observe the short term value instead (e.g. live mixing).

- **`scale`** Sets the display scale for the loudness. Valid parameters are `absolute` (in LUFS) or `relative` (LU) relative to the target. This only affects the video output, not the summary or continuous log output.

- **`integrated`** Read-only exported value for measured integrated loudness, in LUFS.

- **`range`** Read-only exported value for measured loudness range, in LU.

- **`lra_low`** Read-only exported value for measured LRA low, in LUFS.

- **`lra_high`** Read-only exported value for measured LRA high, in LUFS.

- **`sample_peak`** Read-only exported value for measured sample peak, in dBFS.

- **`true_peak`** Read-only exported value for measured true peak, in dBFS.

## Examples

- Real-time graph using `ffplay`, with a EBU scale meter +18:

  ``` text
  ffplay -f lavfi -i "amovie=input.mp3,ebur128=video=1:meter=18 [out0][out1]"
  ```

- Run an analysis with `ffmpeg`:

  ``` text
  ffmpeg -nostats -i input.mp3 -filter_complex ebur128 -f null -
  ```
