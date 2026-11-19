# frei0r

Apply a frei0r effect to the input video.

To enable the compilation of this filter, you need to install the frei0r header and configure FFmpeg with `--enable-frei0r`.

It accepts the following parameters:

- **`filter_name`** The name of the frei0r effect to load. If the environment variable `FREI0R_PATH` is defined, the frei0r effect is searched for in each of the directories specified by the colon-separated list in `FREI0R_PATH`. Otherwise, the standard frei0r paths are searched, in this order: `HOME/.frei0r-1/lib/`, `/usr/local/lib/frei0r-1/`, `/usr/lib/frei0r-1/`.

- **`filter_params`** A '\|'-separated list of parameters to pass to the frei0r effect.

A frei0r effect parameter can be a boolean (its value is either "y" or "n"), a double, a color (specified as \<R\>/\<G\>/\<B\>, where \<R\>, \<G\>, and \<B\> are floating point numbers between 0.0 and 1.0, inclusive) or a color description as specified in the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`, a position (specified as \<X\>/\<Y\>, where \<X\> and \<Y\> are floating point numbers) and/or a string.

The number and types of parameters depend on the loaded effect. If an effect parameter is not specified, the default value is set.

## Examples

- Apply the distort0r effect, setting the first two double parameters:

  ``` text
  frei0r=filter_name=distort0r:filter_params=0.5|0.01
  ```

- Apply the colordistance effect, taking a color as the first parameter:

  ``` text
  frei0r=colordistance:0.2/0.3/0.4
  frei0r=colordistance:violet
  frei0r=colordistance:0x112233
  ```

- Apply the perspective effect, specifying the top left and top right image positions:

  ``` text
  frei0r=perspective:0.2/0.2|0.8/0.2
  ```

For more information, see <http://frei0r.dyne.org>

## Commands

This filter supports the `filter_params` option as [commands](#commands).
