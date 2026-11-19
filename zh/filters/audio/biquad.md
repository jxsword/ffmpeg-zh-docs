# biquad

Apply a biquad IIR filter with the given coefficients. Where \<b0\>, \<b1\>, \<b2\> and \<a0\>, \<a1\>, \<a2\> are the numerator and denominator coefficients respectively. and \<channels\>, \<c\> specify which channels to filter, by default all available are filtered.

## Commands

This filter supports the following commands:

- **`a0`**

- **`a1`**

- **`a2`**

- **`b0`**

- **`b1`**

- **`b2`** Change biquad parameter. Syntax for the command is : "\<value\>"

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
