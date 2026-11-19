# fsync

Synchronize video frames with an external mapping from a file.

For each input PTS given in the map file it either drops or creates as many frames as necessary to recreate the sequence of output frames given in the map file.

This filter is useful to recreate the output frames of a framerate conversion by the [fps](fps.md#fps) filter, recorded into a map file using the ffmpeg option `-stats_mux_pre`, and do further processing to the corresponding frames e.g. quality comparison.

Each line of the map file must contain three items per input frame, the input PTS (decimal), the output PTS (decimal) and the output TIMEBASE (decimal/decimal), separated by a space. This file format corresponds to the output of `-stats_mux_pre_fmt="{ptsi} {pts} {tb}"`.

The filter assumes the map file is sorted by increasing input PTS.

The filter accepts the following options:

| Term      | Description                              |
|-----------|------------------------------------------|
| `file, f` | The filename of the map file to be used. |

Example:

``` text
# Convert a video to 25 fps and record a MAP_FILE file with the default format of this filter
ffmpeg -i INPUT -vf fps=fps=25 -stats_mux_pre MAP_FILE -stats_mux_pre_fmt "{ptsi} {pts} {tb}" OUTPUT

# Sort MAP_FILE by increasing input PTS
sort -n MAP_FILE

# Use INPUT, OUTPUT and the MAP_FILE from above to compare the corresponding frames in INPUT and OUTPUT via SSIM
ffmpeg -i INPUT -i OUTPUT -filter_complex '[0:v]fsync=file=MAP_FILE[ref];[1:v][ref]ssim' -f null -
```
