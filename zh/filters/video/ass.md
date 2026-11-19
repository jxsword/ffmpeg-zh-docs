# ass

Same as the [subtitles](subtitles.md#subtitles) filter, except that it doesn't require libavcodec and libavformat to work. On the other hand, it is limited to ASS (Advanced Substation Alpha) subtitles files.

This filter accepts `filename`/`f`, `original_size`, `fontsdir`, and `alpha` from the [subtitles](subtitles.md#subtitles) filter, plus the following option:

- **`shaping`** Set the shaping engine.

  Available values are:

  - **`auto`** The default libass shaping engine, which is the best available.

  - **`simple`** Fast, font-agnostic shaper that can do only substitutions.

  - **`complex`** Slower shaper using OpenType for substitutions and positioning. Required for correct rendering of complex scripts such as Arabic, Hebrew, Devanagari and Thai. Requires libass to be built with HarfBuzz.

  The default is `auto`.
