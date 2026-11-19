# afade

Apply fade-in/out effect to input audio.

A description of the accepted parameters follows.

- **`type, t`** Specify the effect type, can be either `in` for fade-in, or `out` for a fade-out effect. Default is `in`.

- **`start_sample, ss`** Specify the number of the start sample for starting to apply the fade effect. Default is 0.

- **`nb_samples, ns`** Specify the number of samples for which the fade effect has to last. At the end of the fade-in effect the output audio will have the same volume as the input audio, at the end of the fade-out transition the output audio will be silence. Default is 44100.

- **`start_time, st`** Specify the start time of the fade effect. Default is 0. The value must be specified as a time duration; see section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. If set this option is used instead of \<start_sample\>.

- **`duration, d`** Specify the duration of the fade effect. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. At the end of the fade-in effect the output audio will have the same volume as the input audio, at the end of the fade-out transition the output audio will be silence. By default the duration is determined by \<nb_samples\>. If set this option is used instead of \<nb_samples\>.

- **`curve`** Set curve for fade transition.

  It accepts the following values:

  | Term     | Description                               |
  |----------|-------------------------------------------|
  | `tri`    | select triangular, linear slope (default) |
  | `qsin`   | select quarter of sine wave               |
  | `hsin`   | select half of sine wave                  |
  | `esin`   | select exponential sine wave              |
  | `log`    | select logarithmic                        |
  | `ipar`   | select inverted parabola                  |
  | `qua`    | select quadratic                          |
  | `cub`    | select cubic                              |
  | `squ`    | select square root                        |
  | `cbr`    | select cubic root                         |
  | `par`    | select parabola                           |
  | `exp`    | select exponential                        |
  | `iqsin`  | select inverted quarter of sine wave      |
  | `ihsin`  | select inverted half of sine wave         |
  | `dese`   | select double-exponential seat            |
  | `desi`   | select double-exponential sigmoid         |
  | `losi`   | select logistic sigmoid                   |
  | `sinc`   | select sine cardinal function             |
  | `isinc`  | select inverted sine cardinal function    |
  | `quat`   | select quartic                            |
  | `quatr`  | select quartic root                       |
  | `qsin2`  | select squared quarter of sine wave       |
  | `hsin2`  | select squared half of sine wave          |
  | `nofade` | no fade applied                           |

- **`silence`** Set the initial gain for fade-in or final gain for fade-out. Default value is `0.0`.

- **`unity`** Set the initial gain for fade-out or final gain for fade-in. Default value is `1.0`.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Fade in first 15 seconds of audio:

  ``` text
  afade=t=in:ss=0:d=15
  ```

- Fade out last 25 seconds of a 900 seconds audio:

  ``` text
  afade=t=out:st=875:d=25
  ```
