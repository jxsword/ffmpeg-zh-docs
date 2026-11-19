# zoneplate

Generate a zoneplate test video pattern.

This source accepts the following options:

- **`size, s`** Set frame size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is "320x240".

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`duration, d`** Set the duration of the sourced video. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

  If not specified, or the expressed duration is negative, the video is supposed to be generated forever.

- **`sar`** Set the sample aspect ratio of the sourced video.

- **`precision`** Set precision in bits for look-up table for sine calculations. Default value is 10. Allowed range is from 4 to 16.

- **`xo`** Set horizontal axis offset for output signal. Default value is 0.

- **`yo`** Set vertical axis offset for output signal. Default value is 0.

- **`to`** Set time axis offset for output signal. Default value is 0.

- **`k0`** Set 0-order, constant added to signal phase. Default value is 0.

- **`kx`** Set 1-order, phase factor multiplier for horizontal axis. Default value is 0.

- **`ky`** Set 1-order, phase factor multiplier for vertical axis. Default value is 0.

- **`kt`** Set 1-order, phase factor multiplier for time axis. Default value is 0.

- **`kxt, kyt, kxy`** Set phase factor multipliers for combination of spatial and temporal axis. Default value is 0.

- **`kx2`** Set 2-order, phase factor multiplier for horizontal axis. Default value is 0.

- **`ky2`** Set 2-order, phase factor multiplier for vertical axis. Default value is 0.

- **`kt2`** Set 2-order, phase factor multiplier for time axis. Default value is 0.

- **`ku`** Set the constant added to final phase to produce chroma-blue component of signal. Default value is 0.

- **`kv`** Set the constant added to final phase to produce chroma-red component of signal. Default value is 0.

## Commands

This source supports the some above options as [commands](#commands).

## Examples

- Generate horizontal color sine sweep:

  ``` text
  zoneplate=ku=512:kv=0:kt2=0:kx2=256:s=wvga:xo=-426:kt=11
  ```

- Generate vertical color sine sweep:

  ``` text
  zoneplate=ku=512:kv=0:kt2=0:ky2=156:s=wvga:yo=-240:kt=11
  ```

- Generate circular zone-plate:

  ``` text
  zoneplate=ku=512:kv=100:kt2=0:ky2=256:kx2=556:s=wvga:yo=0:kt=11
  ```
