# readeia608

Read closed captioning (EIA-608) information from the top lines of a video frame.

This filter adds frame metadata for `lavfi.readeia608.X.cc` and `lavfi.readeia608.X.line`, where `X` is the number of the identified line with EIA-608 data (starting from 0). A description of each metadata value follows:

| Term | Description |
|----|----|
| `lavfi.readeia608.X.cc` | The two bytes stored as EIA-608 data (printed in hexadecimal). |
| `lavfi.readeia608.X.line` | The number of the line on which the EIA-608 data was identified and read. |

This filter accepts the following options:

- **`scan_min`** Set the line to start scanning for EIA-608 data. Default is `0`.

- **`scan_max`** Set the line to end scanning for EIA-608 data. Default is `29`.

- **`spw`** Set the ratio of width reserved for sync code detection. Default is `0.27`. Allowed range is `[0.1 - 0.7]`.

- **`chp`** Enable checking the parity bit. In the event of a parity error, the filter will output `0x00` for that character. Default is false.

- **`lp`** Lowpass lines prior to further processing. Default is enabled.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Output a csv with presentation time and the first two lines of identified EIA-608 captioning data.

  ``` text
  ffprobe -f lavfi -i movie=captioned_video.mov,readeia608 -show_entries frame=pts_time:frame_tags=lavfi.readeia608.0.cc,lavfi.readeia608.1.cc -of csv
  ```
