# abuffer

Buffer audio frames, and make them available to the filter chain.

This source is mainly intended for a programmatic use, in particular through the interface defined in `libavfilter/buffersrc.h`.

It accepts the following parameters:

- **`time_base`** The timebase which will be used for timestamps of submitted frames. It must be either a floating-point number or in \<numerator\>/\<denominator\> form.

- **`sample_rate`** The sample rate of the incoming audio buffers.

- **`sample_fmt`** The sample format of the incoming audio buffers. Either a sample format name or its corresponding integer representation from the enum AVSampleFormat in `libavutil/samplefmt.h`

- **`channel_layout`** The channel layout of the incoming audio buffers. Either a channel layout name from channel_layout_map in `libavutil/channel_layout.c` or its corresponding integer representation from the AV_CH_LAYOUT\_\* macros in `libavutil/channel_layout.h`

- **`channels`** The number of channels of the incoming audio buffers. If both \<channels\> and \<channel_layout\> are specified, then they must be consistent.

## Examples

``` text
abuffer=sample_rate=44100:sample_fmt=s16p:channel_layout=stereo
```

will instruct the source to accept planar 16bit signed stereo at 44100Hz. Since the sample format with name "s16p" corresponds to the number 6 and the "stereo" channel layout corresponds to the value 0x3, this is equivalent to:

``` text
abuffer=sample_rate=44100:sample_fmt=6:channel_layout=0x3
```
