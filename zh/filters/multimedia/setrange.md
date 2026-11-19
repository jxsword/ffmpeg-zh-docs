# setrange

Force color range for the output video frame.

The `setrange` filter marks the color range property for the output frames. It does not change the input frame, but only sets the corresponding property, which affects how the frame is treated by following filters.

The filter accepts the following options:

- **`range`** Available values are:

  | Term                     | Description                         |
  |--------------------------|-------------------------------------|
  | `auto`                 | Keep the same color range property. |
  | `unspecified, unknown` | Set the color range as unspecified. |
  | `limited, tv, mpeg`    | Set the color range as limited.     |
  | `full, pc, jpeg`       | Set the color range as full.        |
