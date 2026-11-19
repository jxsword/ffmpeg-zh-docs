# bandreject

Apply a two-pole Butterworth band-reject filter with central frequency \<frequency\>, and (3dB-point) band-width \<width\>. The filter roll off at 6dB per octave (20dB per decade).

The filter accepts the following options:

- **`frequency, f`** Set the filter's central frequency. Default is `3000`.

- **`width_type, t`** Set method to specify band-width of filter.

  | Term | Description |
  |------|-------------|
  | `h`  | Hz          |
  | `q`  | Q-Factor    |
  | `o`  | octave      |
  | `s`  | slope       |
  | `k`  | kHz         |

- **`width, w`** Specify the band-width of a filter in width_type units.

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

## Commands

This filter supports the following commands:

- **`frequency, f`** Change bandreject frequency. Syntax for the command is : "\<frequency\>"

- **`width_type, t`** Change bandreject width_type. Syntax for the command is : "\<width_type\>"

- **`width, w`** Change bandreject width. Syntax for the command is : "\<width\>"

- **`mix, m`** Change bandreject mix. Syntax for the command is : "\<mix\>"
