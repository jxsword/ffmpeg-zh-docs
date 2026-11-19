# subtitles

Draw subtitles on top of input video using the libass library.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libass`. This filter also requires a build with libavcodec and libavformat to convert the passed subtitles file to ASS (Advanced Substation Alpha) subtitles format.

The filter accepts the following options:

- **`filename, f`** Set the filename of the subtitle file to read. It must be specified.

- **`original_size`** Specify the size of the original video, the video for which the ASS file was composed. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Due to a misdesign in ASS aspect ratio arithmetic, this is necessary to correctly scale the fonts if the aspect ratio has been changed.

- **`fontsdir`** Set a directory path containing fonts that can be used by the filter. These fonts will be used in addition to whatever the font provider uses.

- **`alpha`** Process alpha channel, by default alpha channel is untouched.

- **`charenc`** Set subtitles input character encoding. `subtitles` filter only. Only useful if not UTF-8.

- **`stream_index, si`** Set subtitles stream index. `subtitles` filter only.

- **`force_style`** Override default style or script info parameters of the subtitles. It accepts a string containing ASS style format `KEY=VALUE` couples separated by ",".

- **`wrap_unicode`** Break lines according to the Unicode Line Breaking Algorithm. Availability requires at least libass release 0.17.0 (or LIBASS_VERSION 0x01600010), *and* libass must have been built with libunibreak.

  The option is enabled by default except for native ASS.

- **`shaping`** Set the shaping engine.

  Available values are:

  - **`auto`** The default libass shaping engine, which is the best available.

  - **`simple`** Fast, font-agnostic shaper that can do only substitutions.

  - **`complex`** Slower shaper using OpenType for substitutions and positioning. Required for correct rendering of complex scripts such as Arabic, Hebrew, Devanagari and Thai. Requires libass to be built with HarfBuzz.

  The default is `auto`.

If the first key is not specified, it is assumed that the first value specifies the `filename`.

For example, to render the file `sub.srt` on top of the input video, use the command:

``` text
subtitles=sub.srt
```

which is equivalent to:

``` text
subtitles=filename=sub.srt
```

To render the default subtitles stream from file `video.mkv`, use:

``` text
subtitles=video.mkv
```

To render the second subtitles stream from that file, use:

``` text
subtitles=video.mkv:si=1
```

To make the subtitles stream from `sub.srt` appear in 80% transparent blue `DejaVu Serif`, use:

``` text
subtitles=sub.srt:force_style='Fontname=DejaVu Serif,PrimaryColour=&HCCFF0000'
```
