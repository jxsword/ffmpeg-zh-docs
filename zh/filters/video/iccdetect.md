# iccdetect

Detect the colorspace from an embedded ICC profile (if present), and update the frame's tags accordingly.

This filter accepts the following options:

- **`force`** If true, the frame's existing colorspace tags will always be overridden by values detected from an ICC profile. Otherwise, they will only be assigned if they contain `unknown`. Enabled by default.
