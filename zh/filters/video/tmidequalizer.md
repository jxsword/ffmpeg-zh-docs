# tmidequalizer

Apply Temporal Midway Video Equalization effect.

Midway Video Equalization adjusts a sequence of video frames to have the same histograms, while maintaining their dynamics as much as possible. It's useful for e.g. matching exposures from a video frames sequence.

This filter accepts the following option:

- **`radius`** Set filtering radius. Default is `5`. Allowed range is from 1 to 127.

- **`sigma`** Set filtering sigma. Default is `0.5`. This controls strength of filtering. Setting this option to 0 effectively does nothing.

- **`planes`** Set which planes to process. Default is `15`, which is all available planes.
