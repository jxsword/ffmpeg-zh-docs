# fps

Convert the video to specified constant frame rate by duplicating or dropping frames as necessary.

It accepts the following parameters:

- **`fps`** The desired output frame rate. It accepts expressions containing the following constants:

  - **`source_fps`** The input's frame rate

  - **`ntsc`** NTSC frame rate of `30000/1001`

  - **`pal`** PAL frame rate of `25.0`

  - **`film`** Film frame rate of `24.0`

  - **`ntsc_film`** NTSC-film frame rate of `24000/1001`

  The default is `25`.

- **`start_time`** Assume the first PTS should be the given value, in seconds. This allows for padding/trimming at the start of stream. By default, no assumption is made about the first frame's expected PTS, so no padding or trimming is done. For example, this could be set to 0 to pad the beginning with duplicates of the first frame if a video stream starts after the audio stream or to trim any frames with a negative PTS.

- **`round`** Timestamp (PTS) rounding method.

  Possible values are:

  | Term   | Description             |
  |--------|-------------------------|
  | `zero` | round towards 0         |
  | `inf`  | round away from 0       |
  | `down` | round towards -infinity |
  | `up`   | round towards +infinity |
  | `near` | round to nearest        |

  The default is `near`.

- **`eof_action`** Action performed when reading the last frame.

  Possible values are:

  | Term | Description |
  |----|----|
  | `round` | Use same timestamp rounding method as used for other frames. |
  | `pass` | Pass through last frame if input duration has not been reached yet. |

  The default is `round`.

Alternatively, the options can be specified as a flat string: \<fps\>\[:\<start_time\>\[:\<round\>\]\].

See also the [setpts](../overview.md#examples) filter.

## Examples

- A typical usage in order to set the fps to 25:

  ``` text
  fps=fps=25
  ```

- Sets the fps to 24, using abbreviation and rounding method to round to nearest:

  ``` text
  fps=fps=film:round=near
  ```
