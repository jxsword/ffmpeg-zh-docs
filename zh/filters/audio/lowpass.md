# lowpass

Apply a low-pass filter with 3dB point frequency. The filter can be either single-pole or double-pole (the default). The filter roll off at 6dB per pole per octave (20dB per pole per decade).

The filter accepts the following options:

- **`frequency, f`** Set frequency in Hz. Default is 500.

- **`poles, p`** Set number of poles. Default is 2.

- **`width_type, t`** Set method to specify band-width of filter.

  | Term | Description |
  |------|-------------|
  | `h`  | Hz          |
  | `q`  | Q-Factor    |
  | `o`  | octave      |
  | `s`  | slope       |
  | `k`  | kHz         |

- **`width, w`** Specify the band-width of a filter in width_type units. Applies only to double-pole filter. The default is 0.707q and gives a Butterworth response.

- **`mix, m`** How much to use filtered signal in output. Default is 1. Range is between 0 and 1.

- **`channels, c`** Specify which channels to filter, by default all available are filtered.

- **`normalize, n`** Normalize biquad coefficients, by default is disabled. Enabling it will normalize magnitude response at DC to 0dB.

- **`transform, a`** Set transform type of IIR filter.

  - **`di`**

  - **`dii`**

  - **`tdi`**

  - **`tdii`**

  - **`latt`**

  - **`svf`**

  - **`zdf`**

- **`precision, r`** Set precision of filtering.

  | Term   | Description                                                 |
  |--------|-------------------------------------------------------------|
  | `auto` | Pick automatic sample format depending on surround filters. |
  | `s16`  | Always use signed 16-bit.                                   |
  | `s32`  | Always use signed 32-bit.                                   |
  | `f32`  | Always use float 32-bit.                                    |
  | `f64`  | Always use float 64-bit.                                    |

- **`block_size, b`** Set block size used for reverse IIR processing. If this value is set to high enough value (higher than impulse response length truncated when reaches near zero values) filtering will become linear phase otherwise if not big enough it will just produce nasty artifacts.

  Note that filter delay will be exactly this many samples when set to non-zero value.

## Examples

- Lowpass only LFE channel, it LFE is not present it does nothing:

  ``` text
  lowpass=c=LFE
  ```

## Commands

This filter supports the following commands:

- **`frequency, f`** Change lowpass frequency. Syntax for the command is : "\<frequency\>"

- **`width_type, t`** Change lowpass width_type. Syntax for the command is : "\<width_type\>"

- **`width, w`** Change lowpass width. Syntax for the command is : "\<width\>"

- **`mix, m`** Change lowpass mix. Syntax for the command is : "\<mix\>"
