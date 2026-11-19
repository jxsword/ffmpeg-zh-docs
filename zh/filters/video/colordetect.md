# colordetect

Analyze the video frames to determine the effective value range and alpha mode.

The filter accepts the following options:

- **`mode`** Set of properties to detect. Unavailable properties, such as alpha mode for an input image without an alpha channel, will be ignored automatically.

  Accepts a combination of the following flags:

  - **`color_range`** Detect if the source contains luma pixels outside the limited (MPEG) range, which indicates that this is a full range YUV source.

  - **`alpha_mode`** Detect if the source contains color values above the alpha channel, which indicates that the alpha channel is independent (straight), rather than premultiplied. Also detects if the alpha plane is fully opaque or not.

  - **`all`** Enable detection of all of the above properties. This is the default.
