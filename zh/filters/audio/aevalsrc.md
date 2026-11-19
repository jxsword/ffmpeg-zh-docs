# aevalsrc

Generate an audio signal specified by an expression.

This source accepts in input one or more expressions (one for each channel), which are evaluated and used to generate a corresponding audio signal.

This source accepts the following options:

- **`exprs`** Set the '\|'-separated expressions list for each separate channel. In case the `channel_layout` option is not specified, the selected channel layout depends on the number of provided expressions. Otherwise the last specified expression is applied to the remaining output channels.

- **`channel_layout, c`** Set the channel layout. The number of channels in the specified layout must be equal to the number of specified expressions.

- **`duration, d`** Set the minimum duration of the sourced audio. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. Note that the resulting duration may be greater than the specified duration, as the generated audio is always cut at the end of a complete frame.

  If not specified, or the expressed duration is negative, the audio is supposed to be generated forever.

- **`nb_samples, n`** Set the number of samples per channel per each output frame, default to 1024.

- **`sample_rate, s`** Specify the sample rate, default to 44100.

Each expression in \<exprs\> can contain the following constants:

| Term | Description                                                        |
|------|--------------------------------------------------------------------|
| `n`  | number of the evaluated sample, starting from 0                    |
| `t`  | time of the evaluated sample expressed in seconds, starting from 0 |
| `s`  | sample rate                                                        |

## Examples

- Generate silence:

  ``` text
  aevalsrc=0
  ```

- Generate a sin signal with frequency of 440 Hz, set sample rate to 8000 Hz:

  ``` text
  aevalsrc="sin(440*2*PI*t):s=8000"
  ```

- Generate a two channels signal, specify the channel layout (Front Center + Back Center) explicitly:

  ``` text
  aevalsrc="sin(420*2*PI*t)|cos(430*2*PI*t):c=FC|BC"
  ```

- Generate white noise:

  ``` text
  aevalsrc="-2+random(0)"
  ```

- Generate an amplitude modulated signal:

  ``` text
  aevalsrc="sin(10*2*PI*t)*sin(880*2*PI*t)"
  ```

- Generate 2.5 Hz binaural beats on a 360 Hz carrier:

  ``` text
  aevalsrc="0.1*sin(2*PI*(360-2.5/2)*t) | 0.1*sin(2*PI*(360+2.5/2)*t)"
  ```
