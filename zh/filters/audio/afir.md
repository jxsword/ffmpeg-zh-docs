# afir

Apply an arbitrary Finite Impulse Response filter.

This filter is designed for applying long FIR filters, up to 60 seconds long.

It can be used as component for digital crossover filters, room equalization, cross talk cancellation, wavefield synthesis, auralization, ambiophonics, ambisonics and spatialization.

This filter uses the streams higher than first one as FIR coefficients. If the non-first stream holds a single channel, it will be used for all input channels in the first stream, otherwise the number of channels in the non-first stream must be same as the number of channels in the first stream.

It accepts the following parameters:

- **`dry`** Set dry gain. This sets input gain.

- **`wet`** Set wet gain. This sets final output gain.

- **`length`** Set Impulse Response filter length. Default is 1, which means whole IR is processed.

- **`gtype`** This option is deprecated, and does nothing.

- **`irnorm`** Set norm to be applied to IR coefficients before filtering. Allowed range is from \<-1\> to \<2\>. IR coefficients are normalized with calculated vector norm set by this option. For negative values, no norm is calculated, and IR coefficients are not modified at all. Default is \<1\>.

- **`irlink`** For multichannel IR if this option is set to \<true\>, all IR channels will be normalized with maximal measured gain of all IR channels coefficients as set by `irnorm` option. When disabled, all IR coefficients in each IR channel will be normalized independently. Default is \<true\>.

- **`irgain`** Set gain to be applied to IR coefficients before filtering. Allowed range is 0 to 1. This gain is applied after any gain applied with \<irnorm\> option.

- **`irfmt`** Set format of IR stream. Can be `mono` or `input`. Default is `input`.

- **`maxir`** Set max allowed Impulse Response filter duration in seconds. Default is 30 seconds. Allowed range is 0.1 to 60 seconds.

- **`response`** This option is deprecated, and does nothing.

- **`channel`** This option is deprecated, and does nothing.

- **`size`** This option is deprecated, and does nothing.

- **`rate`** This option is deprecated, and does nothing.

- **`minp`** Set minimal partition size used for convolution. Default is \<8192\>. Allowed range is from \<1\> to \<65536\>. Lower values decreases latency at cost of higher CPU usage.

- **`maxp`** Set maximal partition size used for convolution. Default is \<8192\>. Allowed range is from \<8\> to \<65536\>. Lower values may increase CPU usage.

- **`nbirs`** Set number of input impulse responses streams which will be switchable at runtime. Allowed range is from \<1\> to \<32\>. Default is \<1\>.

- **`ir`** Set IR stream which will be used for convolution, starting from \<0\>, should always be lower than supplied value by `nbirs` option. Default is \<0\>. This option can be changed at runtime via [commands](acompressor.md#commands).

- **`precision`** Set which precision to use when processing samples.

  | Term     | Description                                                  |
  |----------|--------------------------------------------------------------|
  | `auto`   | Auto pick internal sample format depending on other filters. |
  | `float`  | Always use single-floating point precision sample format.    |
  | `double` | Always use double-floating point precision sample format.    |

  Default value is auto.

- **`irload`** Set when to load IR stream. Can be `init` or `access`. First one load and prepares all IRs on initialization, second one once on first access of specific IR. Default is `init`.

## Examples

- Apply reverb to stream using mono IR file as second input, complete command using ffmpeg:

  ``` text
  ffmpeg -i input.wav -i middle_tunnel_1way_mono.wav -lavfi afir output.wav
  ```

- Apply true stereo processing given input stereo stream, and two stereo impulse responses for left and right channel, the impulse response files are files with names l_ir.wav and r_ir.wav, and setting irnorm option value:

  ``` text
  "pan=4C|c0=FL|c1=FL|c2=FR|c3=FR[a];amovie=l_ir.wav[LIR];amovie=r_ir.wav[RIR];[LIR][RIR]amerge[ir];[a][ir]afir=irfmt=input:irnorm=1.2,pan=stereo|FL<c0+c2|FR<c1+c3"
  ```

- Similar to above example, but with `irgain` explicitly set to estimated value and with `irnorm` disabled:

  ``` text
  "pan=4C|c0=FL|c1=FL|c2=FR|c3=FR[a];amovie=l_ir.wav[LIR];amovie=r_ir.wav[RIR];[LIR][RIR]amerge[ir];[a][ir]afir=irfmt=input:irgain=-5dB:irnom=-1,pan=stereo|FL<c0+c2|FR<c1+c3"
  ```
