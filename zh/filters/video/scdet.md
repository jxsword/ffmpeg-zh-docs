# scdet

Detect video scene change.

This filter sets frame metadata with mafd between frame, the scene score, and forward the frame to the next filter, so they can use these metadata to detect scene change or others.

In addition, this filter logs a message and sets frame metadata when it detects a scene change by `threshold`.

`lavfi.scd.mafd` metadata keys are set with mafd for every frame.

`lavfi.scd.score` metadata keys are set with scene change score for every frame to detect scene change.

`lavfi.scd.time` metadata keys are set with current filtered frame time which detect scene change with `threshold`.

The filter accepts the following options:

- **`threshold, t`** Set the scene change detection threshold as a percentage of maximum change. Good values are in the `[8.0, 14.0]` range. The range for `threshold` is `[0., 100.]`.

  Default value is `10.`.

- **`sc_pass, s`** Set the flag to pass scene change frames to the next filter. Default value is `0` You can enable it if you want to get snapshot of scene change frames only.
