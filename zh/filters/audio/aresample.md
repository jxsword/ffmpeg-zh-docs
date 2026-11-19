# aresample

Resample the input audio to the specified parameters, using the libswresample library. If none are specified then the filter will automatically convert between its input and output.

This filter is also able to stretch/squeeze the audio data to make it match the timestamps or to inject silence / cut out audio to make it match the timestamps, do a combination of both or do neither.

The filter accepts the syntax \[\<sample_rate\>:\]\<resampler_options\>, where \<sample_rate\> expresses a sample rate and \<resampler_options\> is a list of \<key\>=\<value\> pairs, separated by ":". See the section ""Resampler Options" section in the ffmpeg-resampler(1) manual" in `ffmpeg-resampler` for the complete list of supported options.

## Examples

- Resample the input audio to 44100Hz:

  ``` text
  aresample=44100
  ```

- Stretch/squeeze samples to the given timestamps, with a maximum of 1000 samples per second compensation:

  ``` text
  aresample=async=1000
  ```
