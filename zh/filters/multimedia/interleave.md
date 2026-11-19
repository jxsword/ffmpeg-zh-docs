# interleave, ainterleave

Temporally interleave frames from several inputs.

`interleave` works with video inputs, `ainterleave` with audio.

These filters read frames from several inputs and send the oldest queued frame to the output.

Input streams must have well defined, monotonically increasing frame timestamp values.

In order to submit one frame to output, these filters need to enqueue at least one frame for each input, so they cannot work in case one input is not yet terminated and will not receive incoming frames.

For example consider the case when one input is a `select` filter which always drops input frames. The `interleave` filter will keep reading from that input, but it will never be able to send new frames to output until the input sends an end-of-stream signal.

Also, depending on inputs synchronization, the filters will drop frames in case one input receives more frames than the other ones, and the queue is already filled.

These filters accept the following options:

- **`nb_inputs, n`** Set the number of different inputs, it is 2 by default.

- **`duration`** How to determine the end-of-stream.

  | Term       | Description                                  |
  |------------|----------------------------------------------|
  | `longest`  | The duration of the longest input. (default) |
  | `shortest` | The duration of the shortest input.          |
  | `first`    | The duration of the first input.             |

## Examples

- Interleave frames belonging to different streams using `ffmpeg`:

  ``` text
  ffmpeg -i bambi.avi -i pr0n.mkv -filter_complex "[0:v][1:v] interleave" out.avi
  ```

- Add flickering blur effect:

  ``` text
  select='if(gt(random(0), 0.2), 1, 2)':n=2 [tmp], boxblur=2:2, [tmp] interleave
  ```
