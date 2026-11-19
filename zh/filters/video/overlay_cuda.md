# overlay_cuda

Overlay one video on top of another.

This is the CUDA variant of the [overlay](overlay.md#overlay) filter. It only accepts CUDA frames. The underlying input pixel formats have to match.

It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.

It accepts the following parameters:

- **`x`**

- **`y`** Set expressions for the x and y coordinates of the overlaid video on the main video.

  They can contain the following parameters:

  - **`main_w, W`**

  - **`main_h, H`** The main input width and height.

  - **`overlay_w, w`**

  - **`overlay_h, h`** The overlay input width and height.

  - **`x`**

  - **`y`** The computed values for \<x\> and \<y\>. They are evaluated for each new frame.

  - **`n`** The ordinal index of the main input frame, starting from 0.

  - **`pos`** The byte offset position in the file of the main input frame, NAN if unknown. Deprecated, do not use.

  - **`t`** The timestamp of the main input frame, expressed in seconds, NAN if unknown.

  Default value is "0" for both expressions.

- **`eval`** Set when the expressions for `x` and `y` are evaluated.

  It accepts the following values:

  - **`init`** Evaluate expressions once during filter initialization or when a command is processed.

  - **`frame`** Evaluate expressions for each incoming frame

  Default value is `frame`.

- **`eof_action`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`shortest`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`repeatlast`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.
