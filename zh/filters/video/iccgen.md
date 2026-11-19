# iccgen

Generate ICC profiles and attach them to frames.

This filter accepts the following options:

- **`color_primaries`**

- **`color_trc`** Configure the colorspace that the ICC profile will be generated for. The default value of `auto` infers the value from the input frame's metadata, defaulting to BT.709/sRGB as appropriate.

  See the [setparams](setparams.md#setparams) filter for a list of possible values, but note that `unknown` are not valid values for this filter.

- **`force`** If true, an ICC profile will be generated even if it would overwrite an already existing ICC profile. Disabled by default.
