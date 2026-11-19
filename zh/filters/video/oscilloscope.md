# oscilloscope

2D Video Oscilloscope.

Useful to measure spatial impulse, step responses, chroma delays, etc.

It accepts the following parameters:

| Term | Description |
|----|----|
| `x` | Set scope center x position. |
| `y` | Set scope center y position. |
| `s` | Set scope size, relative to frame diagonal. |
| `t` | Set scope tilt/rotation. |
| `o` | Set trace opacity. |
| `tx` | Set trace center x position. |
| `ty` | Set trace center y position. |
| `tw` | Set trace width, relative to width of frame. |
| `th` | Set trace height, relative to height of frame. |
| `c` | Set which components to trace. By default it traces first three components. |
| `g` | Draw trace grid. By default is enabled. |
| `st` | Draw some statistics. By default is enabled. |
| `sc` | Draw scope. By default is enabled. |

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.

## Examples

- Inspect full first row of video frame.

  ``` text
  oscilloscope=x=0.5:y=0:s=1
  ```

- Inspect full last row of video frame.

  ``` text
  oscilloscope=x=0.5:y=1:s=1
  ```

- Inspect full 5th line of video frame of height 1080.

  ``` text
  oscilloscope=x=0.5:y=5/1080:s=1
  ```

- Inspect full last column of video frame.

  ``` text
  oscilloscope=x=1:y=0.5:s=1:t=1
  ```
