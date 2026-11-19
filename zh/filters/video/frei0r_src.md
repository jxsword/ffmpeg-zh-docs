# frei0r_src

Provide a frei0r source.

To enable compilation of this filter you need to install the frei0r header and configure FFmpeg with `--enable-frei0r`.

This source accepts the following parameters:

- **`size`** The size of the video to generate. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`framerate`** The framerate of the generated video. It may be a string of the form \<num\>/\<den\> or a frame rate abbreviation.

- **`filter_name`** The name to the frei0r source to load. For more information regarding frei0r and how to set the parameters, read the [frei0r](frei0r.md#frei0r) section in the video filters documentation.

- **`filter_params`** A '\|'-separated list of parameters to pass to the frei0r source.

For example, to generate a frei0r partik0l source with size 200x200 and frame rate 10 which is overlaid on the overlay filter main input:

``` text
frei0r_src=size=200x200:framerate=10:filter_name=partik0l:filter_params=1234 [overlay]; [in][overlay] overlay
```
