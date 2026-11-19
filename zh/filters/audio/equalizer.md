# equalizer

Apply a two-pole peaking equalisation (EQ) filter. With this filter, the signal-level at and around a selected frequency can be increased or decreased, whilst (unlike bandpass and bandreject filters) that at all other frequencies is unchanged.

In order to produce complex equalisation curves, this filter can be given several times, each with a different central frequency.

The filter accepts the following options:

- **`frequency, f`** Set the filter's central frequency in Hz.

- **`width_type, t`** Set method to specify band-width of filter.

  | Term | Description |
  |------|-------------|
  | `h`  | Hz          |
  | `q`  | Q-Factor    |
  | `o`  | octave      |
  | `s`  | slope       |
  | `k`  | kHz         |

- **`width, w`** Specify the band-width of a filter in width_type units.

- **`gain, g`** Set the required gain or attenuation in dB. Beware of clipping when using a positive gain.

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

- Attenuate 10 dB at 1000 Hz, with a bandwidth of 200 Hz:

  ``` text
  equalizer=f=1000:t=h:width=200:g=-10
  ```

- Apply 2 dB gain at 1000 Hz with Q 1 and attenuate 5 dB at 100 Hz with Q 2:

  ``` text
  equalizer=f=1000:t=q:w=1:g=2,equalizer=f=100:t=q:w=2:g=-5
  ```

## Commands

This filter supports the following commands:

- **`frequency, f`** Change equalizer frequency. Syntax for the command is : "\<frequency\>"

- **`width_type, t`** Change equalizer width_type. Syntax for the command is : "\<width_type\>"

- **`width, w`** Change equalizer width. Syntax for the command is : "\<width\>"

- **`gain, g`** Change equalizer gain. Syntax for the command is : "\<gain\>"

- **`mix, m`** Change equalizer mix. Syntax for the command is : "\<mix\>"
