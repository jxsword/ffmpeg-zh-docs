# bass, lowshelf

Boost or cut the bass (lower) frequencies of the audio using a two-pole shelving filter with a response similar to that of a standard hi-fi's tone-controls. This is also known as shelving equalisation (EQ).

The filter accepts the following options:

- **`gain, g`** Give the gain at 0 Hz. Its useful range is about -20 (for a large cut) to +20 (for a large boost). Beware of clipping when using a positive gain.

- **`frequency, f`** Set the filter's central frequency and so can be used to extend or reduce the frequency range to be boosted or cut. The default value is `100` Hz.

- **`width_type, t`** Set method to specify band-width of filter.

  | Term | Description |
  |------|-------------|
  | `h`  | Hz          |
  | `q`  | Q-Factor    |
  | `o`  | octave      |
  | `s`  | slope       |
  | `k`  | kHz         |

- **`width, w`** Determine how steep is the filter's shelf transition.

- **`poles, p`** Set number of poles. Default is 2.

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

- **`frequency, f`** Change bass frequency. Syntax for the command is : "\<frequency\>"

- **`width_type, t`** Change bass width_type. Syntax for the command is : "\<width_type\>"

- **`width, w`** Change bass width. Syntax for the command is : "\<width\>"

- **`gain, g`** Change bass gain. Syntax for the command is : "\<gain\>"

- **`mix, m`** Change bass mix. Syntax for the command is : "\<mix\>"
