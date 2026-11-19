# anullsrc

The null audio source, return unprocessed audio frames. It is mainly useful as a template and to be employed in analysis / debugging tools, or as the source for filters which ignore the input data (for example the sox synth filter).

This source accepts the following options:

- **`channel_layout, cl`** Specifies the channel layout, and can be either an integer or a string representing a channel layout. The default value of \<channel_layout\> is "stereo".

  Check the channel_layout_map definition in `libavutil/channel_layout.c` for the mapping between strings and channel layout values.

- **`sample_rate, r`** Specifies the sample rate, and defaults to 44100.

- **`nb_samples, n`** Set the number of samples per requested frames.

- **`duration, d`** Set the duration of the sourced audio. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

  If not specified, or the expressed duration is negative, the audio is supposed to be generated forever.

## Examples

- Set the sample rate to 48000 Hz and the channel layout to AV_CH_LAYOUT_MONO.

  ``` text
  anullsrc=r=48000:cl=4
  ```

- Do the same operation with a more obvious syntax:

  ``` text
  anullsrc=r=48000:cl=mono
  ```

All the parameters need to be explicitly defined.
