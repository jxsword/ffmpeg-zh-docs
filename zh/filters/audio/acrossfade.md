# acrossfade

Apply cross fade from one input audio stream to another input audio stream. The cross fade is applied for specified duration near the end of first stream.

The filter accepts the following options:

- **`inputs, n`** Specify the number of inputs to crossfade. When crossfading multiple inputs, each input will be concatenated and crossfaded in sequence, similar to the [concat filter](../overview.md#examples). Default is 2.

- **`nb_samples, ns`** Specify the number of samples for which the cross fade effect has to last. At the end of the cross fade effect the first input audio will be completely silent. Default is 44100.

- **`duration, d`** Specify the duration of the cross fade effect. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. By default the duration is determined by \<nb_samples\>. If set this option is used instead of \<nb_samples\>.

- **`overlap, o`** Should first stream end overlap with second stream start. Default is enabled.

- **`curve1`** Set curve for cross fade transition for first stream.

- **`curve2`** Set curve for cross fade transition for second stream.

  For description of available curve types see [afade](afade.md#afade) filter description.

## Examples

- Cross fade from one input to another:

  ``` text
  ffmpeg -i first.flac -i second.flac -filter_complex acrossfade=d=10:c1=exp:c2=exp output.flac
  ```

- Cross fade from one input to another but without overlapping:

  ``` text
  ffmpeg -i first.flac -i second.flac -filter_complex acrossfade=d=10:o=0:c1=exp:c2=exp output.flac
  ```

  Concatenate multiple inputs with cross fade between each:

  ``` text
  ffmpeg -i first.flac -i second.flac -i third.flac -filter_complex acrossfade=n=3 output.flac
  ```
