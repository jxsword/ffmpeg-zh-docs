# haas

Apply Haas effect to audio.

Note that this makes most sense to apply on mono signals. With this filter applied to mono signals it give some directionality and stretches its stereo image.

The filter accepts the following options:

- **`level_in`** Set input level. By default is \<1\>, or 0dB

- **`level_out`** Set output level. By default is \<1\>, or 0dB.

- **`side_gain`** Set gain applied to side part of signal. By default is \<1\>.

- **`middle_source`** Set kind of middle source. Can be one of the following:

  | Term      | Description                              |
  |-----------|------------------------------------------|
  | `left`  | Pick left channel.                       |
  | `right` | Pick right channel.                      |
  | `mid`   | Pick middle part signal of stereo image. |
  | `side`  | Pick side part signal of stereo image.   |

- **`middle_phase`** Change middle phase. By default is disabled.

- **`left_delay`** Set left channel delay. By default is \<2.05\> milliseconds.

- **`left_balance`** Set left channel balance. By default is \<-1\>.

- **`left_gain`** Set left channel gain. By default is \<1\>.

- **`left_phase`** Change left phase. By default is disabled.

- **`right_delay`** Set right channel delay. By defaults is \<2.12\> milliseconds.

- **`right_balance`** Set right channel balance. By default is \<1\>.

- **`right_gain`** Set right channel gain. By default is \<1\>.

- **`right_phase`** Change right phase. By default is enabled.
