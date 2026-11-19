# drawgraph

Draw a graph using input video metadata.

It accepts the following parameters:

- **`m1`** Set 1st frame metadata key from which metadata values will be used to draw a graph.

- **`fg1`** Set 1st foreground color expression.

- **`m2`** Set 2nd frame metadata key from which metadata values will be used to draw a graph.

- **`fg2`** Set 2nd foreground color expression.

- **`m3`** Set 3rd frame metadata key from which metadata values will be used to draw a graph.

- **`fg3`** Set 3rd foreground color expression.

- **`m4`** Set 4th frame metadata key from which metadata values will be used to draw a graph.

- **`fg4`** Set 4th foreground color expression.

- **`min`** Set minimal value of metadata value.

- **`max`** Set maximal value of metadata value.

- **`bg`** Set graph background color. Default is white.

- **`mode`** Set graph mode.

  Available values for mode is:

  - **`bar`**

  - **`dot`**

  - **`line`**

  Default is `line`.

- **`slide`** Set slide mode.

  Available values for slide is:

  | Term        | Description                                  |
  |-------------|----------------------------------------------|
  | `frame`   | Draw new frame when right border is reached. |
  | `replace` | Replace old columns with new ones.           |
  | `scroll`  | Scroll from right to left.                   |
  | `rscroll` | Scroll from left to right.                   |
  | `picture` | Draw single picture.                         |

  Default is `frame`.

- **`size`** Set size of graph video. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. The default value is `900x256`.

- **`rate, r`** Set the output frame rate. Default value is `25`.

  The foreground color expressions can use the following variables:

  | Term  | Description                      |
  |-------|----------------------------------|
  | `MIN` | Minimal value of metadata value. |
  | `MAX` | Maximal value of metadata value. |
  | `VAL` | Current metadata key value.      |

  The color is defined as 0xAABBGGRR.

Example using metadata from [signalstats](signalstats.md#signalstats) filter:

``` text
signalstats,drawgraph=lavfi.signalstats.YAVG:min=0:max=255
```

Example using metadata from [ebur128](../multimedia/ebur128.md#ebur128) filter:

``` text
ebur128=metadata=1,adrawgraph=lavfi.r128.M:min=-120:max=5
```
