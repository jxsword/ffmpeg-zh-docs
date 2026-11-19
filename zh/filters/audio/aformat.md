# aformat

Set output format constraints for the input audio. The framework will negotiate the most appropriate format to minimize conversions.

It accepts the following parameters:

- **`sample_fmts, f`** A '\|'-separated list of requested sample formats.

- **`sample_rates, r`** A '\|'-separated list of requested sample rates.

- **`channel_layouts, cl`** A '\|'-separated list of requested channel layouts.

  See section "the Channel Layout section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the required syntax.

If a parameter is omitted, all values are allowed.

Force the output to either unsigned 8-bit or signed 16-bit stereo

``` text
aformat=sample_fmts=u8|s16:channel_layouts=stereo
```
