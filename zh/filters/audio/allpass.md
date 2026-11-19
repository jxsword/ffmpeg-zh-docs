# allpass

Apply a two-pole all-pass filter with central frequency (in Hz) \<frequency\>, and filter-width \<width\>. An all-pass filter changes the audio's frequency to phase relationship without changing its frequency to amplitude relationship.

The filter accepts the following options:

- **`frequency, f`** Set frequency in Hz.

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

- **`order, o`** Set the filter order, can be 1 or 2. Default is 2.

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

## Commands

This filter supports the following commands:

- **`frequency, f`** Change allpass frequency. Syntax for the command is : "\<frequency\>"

- **`width_type, t`** Change allpass width_type. Syntax for the command is : "\<width_type\>"

- **`width, w`** Change allpass width. Syntax for the command is : "\<width\>"

- **`mix, m`** Change allpass mix. Syntax for the command is : "\<mix\>"
