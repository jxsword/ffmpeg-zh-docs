# aiir

Apply an arbitrary Infinite Impulse Response filter.

It accepts the following parameters:

- **`zeros, z`** Set B/numerator/zeros/reflection coefficients.

- **`poles, p`** Set A/denominator/poles/ladder coefficients.

- **`gains, k`** Set channels gains.

- **`dry_gain`** Set input gain.

- **`wet_gain`** Set output gain.

- **`format, f`** Set coefficients format.

  | Term   | Description                              |
  |--------|------------------------------------------|
  | `ll` | lattice-ladder function                  |
  | `sf` | analog transfer function                 |
  | `tf` | digital transfer function                |
  | `zp` | Z-plane zeros/poles, cartesian (default) |
  | `pr` | Z-plane zeros/poles, polar radians       |
  | `pd` | Z-plane zeros/poles, polar degrees       |
  | `sp` | S-plane zeros/poles                      |

- **`process, r`** Set type of processing.

  | Term  | Description         |
  |-------|---------------------|
  | `d` | direct processing   |
  | `s` | serial processing   |
  | `p` | parallel processing |

- **`precision, e`** Set filtering precision.

  | Term    | Description                               |
  |---------|-------------------------------------------|
  | `dbl` | double-precision floating-point (default) |
  | `flt` | single-precision floating-point           |
  | `i32` | 32-bit integers                           |
  | `i16` | 16-bit integers                           |

- **`normalize, n`** Normalize filter coefficients, by default is enabled. Enabling it will normalize magnitude response at DC to 0dB.

- **`mix`** How much to use filtered signal in output. Default is 1. Range is between 0 and 1.

- **`response`** Show IR frequency response, magnitude(magenta), phase(green) and group delay(yellow) in additional video stream. By default it is disabled.

- **`channel`** Set for which IR channel to display frequency response. By default is first channel displayed. This option is used only when \<response\> is enabled.

- **`size`** Set video stream size. This option is used only when \<response\> is enabled.

Coefficients in `tf` and `sf` format are separated by spaces and are in ascending order.

Coefficients in `zp` format are separated by spaces and order of coefficients doesn't matter. Coefficients in `zp` format are complex numbers with \<i\> imaginary unit.

Different coefficients and gains can be provided for every channel, in such case use '\|' to separate coefficients or gains. Last provided coefficients will be used for all remaining channels.

## Examples

- Apply 2 pole elliptic notch at around 5000Hz for 48000 Hz sample rate:

  ``` text
  aiir=k=1:z=7.957584807809675810E-1 -2.575128568908332300 3.674839853930788710 -2.57512875289799137 7.957586296317130880E-1:p=1 -2.86950072432325953 3.63022088054647218 -2.28075678147272232 6.361362326477423500E-1:f=tf:r=d
  ```

- Same as above but in `zp` format:

  ``` text
  aiir=k=0.79575848078096756:z=0.80918701+0.58773007i 0.80918701-0.58773007i 0.80884700+0.58784055i 0.80884700-0.58784055i:p=0.63892345+0.59951235i 0.63892345-0.59951235i 0.79582691+0.44198673i 0.79582691-0.44198673i:f=zp:r=s
  ```

- Apply 3-rd order analog normalized Butterworth low-pass filter, using analog transfer function format:

  ``` text
  aiir=z=1.3057 0 0 0:p=1.3057 2.3892 2.1860 1:f=sf:r=d
  ```
