# framepack

Pack two different video streams into a stereoscopic video, setting proper metadata on supported codecs. The two views should have the same size and framerate and processing will stop when the shorter video ends. Please note that you may conveniently adjust view properties with the [scale](scale.md#scale) and [fps](fps.md#fps) filters.

It accepts the following parameters:

- **`format`** The desired packing format. Supported values are:

  | Term       | Description                                 |
  |------------|---------------------------------------------|
  | `sbs`      | The views are next to each other (default). |
  | `tab`      | The views are on top of each other.         |
  | `lines`    | The views are packed by line.               |
  | `columns`  | The views are packed by column.             |
  | `frameseq` | The views are temporally interleaved.       |

Some examples:

``` text
# Convert left and right views into a frame-sequential video
ffmpeg -i LEFT -i RIGHT -filter_complex framepack=frameseq OUTPUT

# Convert views into a side-by-side video with the same output resolution as the input
ffmpeg -i LEFT -i RIGHT -filter_complex [0:v]scale=w=iw/2[left],[1:v]scale=w=iw/2[right],[left][right]framepack=sbs OUTPUT
```
