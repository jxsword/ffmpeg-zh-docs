# showvolume

Convert input audio volume to a video output.

The filter accepts the following options:

- **`rate, r`** Set video rate.

- **`b`** Set border width, allowed range is \[0, 5\]. Default is 1.

- **`w`** Set channel width, allowed range is \[80, 8192\]. Default is 400.

- **`h`** Set channel height, allowed range is \[1, 900\]. Default is 20.

- **`f`** Set fade, allowed range is \[0, 1\]. Default is 0.95.

- **`c`** Set volume color expression.

  The expression can use the following variables:

  | Term      | Description                              |
  |-----------|------------------------------------------|
  | `VOLUME`  | Current max volume of channel in dB.     |
  | `PEAK`    | Current peak.                            |
  | `CHANNEL` | Current channel number, starting from 0. |

- **`t`** If set, displays channel names. Default is enabled.

- **`v`** If set, displays volume values. Default is enabled.

- **`o`** Set orientation, can be horizontal: `h` or vertical: `v`, default is `h`.

- **`s`** Set step size, allowed range is \[0, 5\]. Default is 0, which means step is disabled.

- **`p`** Set background opacity, allowed range is \[0, 1\]. Default is 0.

- **`m`** Set metering mode, can be peak: `p` or rms: `r`, default is `p`.

- **`ds`** Set display scale, can be linear: `lin` or log: `log`, default is `lin`.

- **`dm`** In second. If set to \> 0., display a line for the max level in the previous seconds. default is disabled: `0.`

- **`dmc`** The color of the max line. Use when `dm` option is set to \> 0. default is: `orange`
