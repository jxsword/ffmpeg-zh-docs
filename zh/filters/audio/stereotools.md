# stereotools

This filter has some handy utilities to manage stereo signals, for converting M/S stereo recordings to L/R signal while having control over the parameters or spreading the stereo image of master track.

The filter accepts the following options:

- **`level_in`** Set input level before filtering for both channels. Defaults is 1. Allowed range is from 0.015625 to 64.

- **`level_out`** Set output level after filtering for both channels. Defaults is 1. Allowed range is from 0.015625 to 64.

- **`balance_in`** Set input balance between both channels. Default is 0. Allowed range is from -1 to 1.

- **`balance_out`** Set output balance between both channels. Default is 0. Allowed range is from -1 to 1.

- **`softclip`** Enable softclipping. Results in analog distortion instead of harsh digital 0dB clipping. Disabled by default.

- **`mutel`** Mute the left channel. Disabled by default.

- **`muter`** Mute the right channel. Disabled by default.

- **`phasel`** Change the phase of the left channel. Disabled by default.

- **`phaser`** Change the phase of the right channel. Disabled by default.

- **`mode`** Set stereo mode. Available values are:

  | Term       | Description                                |
  |------------|--------------------------------------------|
  | `lr>lr`  | Left/Right to Left/Right, this is default. |
  | `lr>ms`  | Left/Right to Mid/Side.                    |
  | `ms>lr`  | Mid/Side to Left/Right.                    |
  | `lr>ll`  | Left/Right to Left/Left.                   |
  | `lr>rr`  | Left/Right to Right/Right.                 |
  | `lr>l+r` | Left/Right to Left + Right.                |
  | `lr>rl`  | Left/Right to Right/Left.                  |
  | `ms>ll`  | Mid/Side to Left/Left.                     |
  | `ms>rr`  | Mid/Side to Right/Right.                   |
  | `ms>rl`  | Mid/Side to Right/Left.                    |
  | `lr>l-r` | Left/Right to Left - Right.                |

- **`slev`** Set level of side signal. Default is 1. Allowed range is from 0.015625 to 64.

- **`sbal`** Set balance of side signal. Default is 0. Allowed range is from -1 to 1.

- **`mlev`** Set level of the middle signal. Default is 1. Allowed range is from 0.015625 to 64.

- **`mpan`** Set middle signal pan. Default is 0. Allowed range is from -1 to 1.

- **`base`** Set stereo base between mono and inversed channels. Default is 0. Allowed range is from -1 to 1.

- **`delay`** Set delay in milliseconds how much to delay left from right channel and vice versa. Default is 0. Allowed range is from -20 to 20.

- **`sclevel`** Set S/C level. Default is 1. Allowed range is from 1 to 100.

- **`phase`** Set the stereo phase in degrees. Default is 0. Allowed range is from 0 to 360.

- **`bmode_in, bmode_out`** Set balance mode for balance_in/balance_out option.

  Can be one of the following:

  | Term | Description |
  |----|----|
  | `balance` | Classic balance mode. Attenuate one channel at time. Gain is raised up to 1. |
  | `amplitude` | Similar as classic mode above but gain is raised up to 2. |
  | `power` | Equal power distribution, from -6dB to +6dB range. |

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Apply karaoke like effect:

  ``` text
  stereotools=mlev=0.015625
  ```

- Convert M/S signal to L/R:

  ``` text
  "stereotools=mode=ms>lr"
  ```
