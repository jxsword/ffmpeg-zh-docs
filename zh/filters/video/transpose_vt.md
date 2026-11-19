# transpose_vt

Transpose rows with columns in the input video and optionally flip it. For more in depth examples see the [transpose](transpose.md#transpose) video filter, which shares mostly the same options.

It accepts the following parameters:

- **`dir`** Specify the transposition direction.

  Can assume the following values:

  | Term | Description |
  |----|----|
  | `cclock_flip` | Rotate by 90 degrees counterclockwise and vertically flip. (default) |
  | `clock` | Rotate by 90 degrees clockwise. |
  | `cclock` | Rotate by 90 degrees counterclockwise. |
  | `clock_flip` | Rotate by 90 degrees clockwise and vertically flip. |
  | `hflip` | Flip the input video horizontally. |
  | `vflip` | Flip the input video vertically. |

- **`passthrough`** Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values:

  - **`none`** Always apply transposition. (default)

  - **`portrait`** Preserve portrait geometry (when \<height\> \>= \<width\>).

  - **`landscape`** Preserve landscape geometry (when \<width\> \>= \<height\>).
