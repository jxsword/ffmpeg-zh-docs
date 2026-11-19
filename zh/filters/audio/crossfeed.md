# crossfeed

Apply headphone crossfeed filter.

Crossfeed is the process of blending the left and right channels of stereo audio recording. It is mainly used to reduce extreme stereo separation of low frequencies.

The intent is to produce more speaker like sound to the listener.

The filter accepts the following options:

- **`strength`** Set strength of crossfeed. Default is 0.2. Allowed range is from 0 to 1. This sets gain of low shelf filter for side part of stereo image. Default is -6dB. Max allowed is -30db when strength is set to 1.

- **`range`** Set soundstage wideness. Default is 0.5. Allowed range is from 0 to 1. This sets cut off frequency of low shelf filter. Default is cut off near 1550 Hz. With range set to 1 cut off frequency is set to 2100 Hz.

- **`slope`** Set curve slope of low shelf filter. Default is 0.5. Allowed range is from 0.01 to 1.

- **`level_in`** Set input gain. Default is 0.9.

- **`level_out`** Set output gain. Default is 1.

- **`block_size`** Set block size used for reverse IIR processing. If this value is set to high enough value (higher than impulse response length truncated when reaches near zero values) filtering will become linear phase otherwise if not big enough it will just produce nasty artifacts.

  Note that filter delay will be exactly this many samples when set to non-zero value.

## Commands

This filter supports the all above options as [commands](#commands).
