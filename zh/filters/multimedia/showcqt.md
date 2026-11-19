# showcqt

Convert input audio to a video output representing frequency spectrum logarithmically using Brown-Puckette constant Q transform algorithm with direct frequency domain coefficient calculation (but the transform itself is not really constant Q, instead the Q factor is actually variable/clamped), with musical tone scale, from E0 to D#10.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. It must be even. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `1920x1080`.

- **`fps, rate, r`** Set the output frame rate. Default value is `25`.

- **`bar_h`** Set the bargraph height. It must be even. Default value is `-1` which computes the bargraph height automatically.

- **`axis_h`** Set the axis height. It must be even. Default value is `-1` which computes the axis height automatically.

- **`sono_h`** Set the sonogram height. It must be even. Default value is `-1` which computes the sonogram height automatically.

- **`fullhd`** Set the fullhd resolution. This option is deprecated, use \<size\>, \<s\> instead. Default value is `1`.

- **`sono_v, volume`** Specify the sonogram volume expression. It can contain variables:

  - **`bar_v`** the \<bar_v\> evaluated expression

  - **`frequency, freq, f`** the frequency where it is evaluated

  - **`timeclamp, tc`** the value of \<timeclamp\> option

  and functions:

  | Term             | Description                    |
  |------------------|--------------------------------|
  | `a_weighting(f)` | A-weighting of equal loudness  |
  | `b_weighting(f)` | B-weighting of equal loudness  |
  | `c_weighting(f)` | C-weighting of equal loudness. |

  Default value is `16`.

- **`bar_v, volume2`** Specify the bargraph volume expression. It can contain variables:

  - **`sono_v`** the \<sono_v\> evaluated expression

  - **`frequency, freq, f`** the frequency where it is evaluated

  - **`timeclamp, tc`** the value of \<timeclamp\> option

  and functions:

  | Term             | Description                    |
  |------------------|--------------------------------|
  | `a_weighting(f)` | A-weighting of equal loudness  |
  | `b_weighting(f)` | B-weighting of equal loudness  |
  | `c_weighting(f)` | C-weighting of equal loudness. |

  Default value is `sono_v`.

- **`sono_g, gamma`** Specify the sonogram gamma. Lower gamma makes the spectrum more contrast, higher gamma makes the spectrum having more range. Default value is `3`. Acceptable range is `[1, 7]`.

- **`bar_g, gamma2`** Specify the bargraph gamma. Default value is `1`. Acceptable range is `[1, 7]`.

- **`bar_t`** Specify the bargraph transparency level. Lower value makes the bargraph sharper. Default value is `1`. Acceptable range is `[0, 1]`.

- **`timeclamp, tc`** Specify the transform timeclamp. At low frequency, there is trade-off between accuracy in time domain and frequency domain. If timeclamp is lower, event in time domain is represented more accurately (such as fast bass drum), otherwise event in frequency domain is represented more accurately (such as bass guitar). Acceptable range is `[0.002, 1]`. Default value is `0.17`.

- **`attack`** Set attack time in seconds. The default is `0` (disabled). Otherwise, it limits future samples by applying asymmetric windowing in time domain, useful when low latency is required. Accepted range is `[0, 1]`.

- **`basefreq`** Specify the transform base frequency. Default value is `20.01523126408007475`, which is frequency 50 cents below E0. Acceptable range is `[10, 100000]`.

- **`endfreq`** Specify the transform end frequency. Default value is `20495.59681441799654`, which is frequency 50 cents above D#10. Acceptable range is `[10, 100000]`.

- **`coeffclamp`** This option is deprecated and ignored.

- **`tlength`** Specify the transform length in time domain. Use this option to control accuracy trade-off between time domain and frequency domain at every frequency sample. It can contain variables:

  - **`frequency, freq, f`** the frequency where it is evaluated

  - **`timeclamp, tc`** the value of \<timeclamp\> option.

  Default value is `384*tc/(384+tc*f)`.

- **`count`** Specify the transform count for every video frame. Default value is `6`. Acceptable range is `[1, 30]`.

- **`fcount`** Specify the transform count for every single pixel. Default value is `0`, which makes it computed automatically. Acceptable range is `[0, 10]`.

- **`fontfile`** Specify font file for use with freetype to draw the axis. If not specified, use embedded font. Note that drawing with font file or embedded font is not implemented with custom \<basefreq\> and \<endfreq\>, use \<axisfile\> option instead.

- **`font`** Specify fontconfig pattern. This has lower priority than \<fontfile\>. The `:` in the pattern may be replaced by `|` to avoid unnecessary escaping.

- **`fontcolor`** Specify font color expression. This is arithmetic expression that should return integer value 0xRRGGBB. It can contain variables:

  - **`frequency, freq, f`** the frequency where it is evaluated

  - **`timeclamp, tc`** the value of \<timeclamp\> option

  and functions:

  | Term | Description |
  |----|----|
  | `midi(f)` | midi number of frequency f, some midi numbers: E0(16), C1(24), C2(36), A4(69) |
  | `r(x), g(x), b(x)` | red, green, and blue value of intensity x. |

  Default value is `st(0, (midi(f)-59.5)/12); st(1, if(between(ld(0),0,1), 0.5-0.5*cos(2*PI*ld(0)), 0)); r(1-ld(1)) + b(ld(1))`.

- **`axisfile`** Specify image file to draw the axis. This option override \<fontfile\> and \<fontcolor\> option.

- **`axis, text`** Enable/disable drawing text to the axis. If it is set to `0`, drawing to the axis is disabled, ignoring \<fontfile\> and \<axisfile\> option. Default value is `1`.

- **`csp`** Set colorspace. The accepted values are:

  | Term            | Description                         |
  |-----------------|-------------------------------------|
  | `unspecified` | Unspecified (default)               |
  | `bt709`       | BT.709                              |
  | `fcc`         | FCC                                 |
  | `bt470bg`     | BT.470BG or BT.601-6 625            |
  | `smpte170m`   | SMPTE-170M or BT.601-6 525          |
  | `smpte240m`   | SMPTE-240M                          |
  | `bt2020ncl`   | BT.2020 with non-constant luminance |

- **`cscheme`** Set spectrogram color scheme. This is list of floating point values with format `left_r|left_g|left_b|right_r|right_g|right_b`. The default is `1|0.5|0|0|0.5|1`.

## Examples

- Playing audio while showing the spectrum:

  ``` text
  ffplay -f lavfi 'amovie=a.mp3, asplit [a][out1]; [a] showcqt [out0]'
  ```

- Same as above, but with frame rate 30 fps:

  ``` text
  ffplay -f lavfi 'amovie=a.mp3, asplit [a][out1]; [a] showcqt=fps=30:count=5 [out0]'
  ```

- Playing at 1280x720:

  ``` text
  ffplay -f lavfi 'amovie=a.mp3, asplit [a][out1]; [a] showcqt=s=1280x720:count=4 [out0]'
  ```

- Disable sonogram display:

  ``` text
  sono_h=0
  ```

- A1 and its harmonics: A1, A2, (near)E3, A3:

  ``` c
  ffplay -f lavfi 'aevalsrc=0.1*sin(2*PI*55*t)+0.1*sin(4*PI*55*t)+0.1*sin(6*PI*55*t)+0.1*sin(8*PI*55*t),
                   asplit[a][out1]; [a] showcqt [out0]'
  ```

- Same as above, but with more accuracy in frequency domain:

  ``` c
  ffplay -f lavfi 'aevalsrc=0.1*sin(2*PI*55*t)+0.1*sin(4*PI*55*t)+0.1*sin(6*PI*55*t)+0.1*sin(8*PI*55*t),
                   asplit[a][out1]; [a] showcqt=timeclamp=0.5 [out0]'
  ```

- Custom volume:

  ``` text
  bar_v=10:sono_v=bar_v*a_weighting(f)
  ```

- Custom gamma, now spectrum is linear to the amplitude.

  ``` text
  bar_g=2:sono_g=2
  ```

- Custom tlength equation:

  ``` c
  tc=0.33:tlength='st(0,0.17); 384*tc / (384 / ld(0) + tc*f /(1-ld(0))) + 384*tc / (tc*f / ld(0) + 384 /(1-ld(0)))'
  ```

- Custom fontcolor and fontfile, C-note is colored green, others are colored blue:

  ``` text
  fontcolor='if(mod(floor(midi(f)+0.5),12), 0x0000FF, g(1))':fontfile=myfont.ttf
  ```

- Custom font using fontconfig:

  ``` text
  font='Courier New,Monospace,mono|bold'
  ```

- Custom frequency range with custom axis using image file:

  ``` text
  axisfile=myaxis.png:basefreq=40:endfreq=10000
  ```
