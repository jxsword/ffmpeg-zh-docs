# setfield

Force field for the output video frame.

The `setfield` filter marks the interlace type field for the output frames. It does not change the input frame, but only sets the corresponding property, which affects how the frame is treated by following filters (e.g. `fieldorder` or `yadif`).

The filter accepts the following options:

- **`mode`** Available values are:

  | Term     | Description                           |
  |----------|---------------------------------------|
  | `auto` | Keep the same field property.         |
  | `bff`  | Mark the frame as bottom-field-first. |
  | `tff`  | Mark the frame as top-field-first.    |
  | `prog` | Mark the frame as progressive.        |
