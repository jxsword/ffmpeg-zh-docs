# adenorm

Remedy denormals in audio by adding extremely low-level noise.

This filter shall be placed before any filter that can produce denormals.

A description of the accepted parameters follows.

- **`level`** Set level of added noise in dB. Default is `-351`. Allowed range is from -451 to -90.

- **`type`** Set type of added noise.

  | Term     | Description        |
  |----------|--------------------|
  | `dc`     | Add DC signal.     |
  | `ac`     | Add AC signal.     |
  | `square` | Add square signal. |
  | `pulse`  | Add pulse signal.  |

  Default is `dc`.

## Commands

This filter supports the all above options as [commands](#commands).
