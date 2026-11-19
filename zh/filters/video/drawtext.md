# drawtext

Draw a text string or text from a specified file on top of a video, using the libfreetype library.

To enable compilation of this filter, you need to configure FFmpeg with `--enable-libfreetype` and `--enable-libharfbuzz`. To enable default font fallback and the \<font\> option you need to configure FFmpeg with `--enable-libfontconfig`. To enable the \<text_shaping\> option, you need to configure FFmpeg with `--enable-libfribidi`.

## Syntax

It accepts the following parameters:

- **`box`** Used to draw a box around text using the background color. The value must be either 1 (enable) or 0 (disable). The default value of \<box\> is 0.

- **`boxborderw`** Set the width of the border to be drawn around the box using \<boxcolor\>. The value must be specified using one of the following formats:

  - `boxborderw=10` set the width of all the borders to 10

  - `boxborderw=10|20` set the width of the top and bottom borders to 10 and the width of the left and right borders to 20

  - `boxborderw=10|20|30` set the width of the top border to 10, the width of the bottom border to 30 and the width of the left and right borders to 20

  - `boxborderw=10|20|30|40` set the borders width to 10 (top), 20 (right), 30 (bottom), 40 (left)

  The default value of \<boxborderw\> is "0".

- **`boxcolor`** The color to be used for drawing box around text. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<boxcolor\> is "white".

- **`line_spacing`** Set the line spacing in pixels. The default value of \<line_spacing\> is 0.

- **`text_align`** Set the vertical and horizontal alignment of the text with respect to the box boundaries. The value is combination of flags, one for the vertical alignment (T=top, M=middle, B=bottom) and one for the horizontal alignment (L=left, C=center, R=right). Please note that tab characters are only supported with the left horizontal alignment.

- **`y_align`** Specify what the \<y\> value is referred to. Possible values are:

  - `text` the top of the highest glyph of the first text line is placed at \<y\>

  - `baseline` the baseline of the first text line is placed at \<y\>

  - `font` the baseline of the first text line is placed at \<y\> plus the ascent (in pixels) defined in the font metrics

  The default value of \<y_align\> is "text" for backward compatibility.

- **`borderw`** Set the width of the border to be drawn around the text using \<bordercolor\>. The default value of \<borderw\> is 0.

- **`bordercolor`** Set the color to be used for drawing border around text. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<bordercolor\> is "black".

- **`expansion`** Select how the \<text\> is expanded. Can be either `none`, `strftime` (deprecated) or `normal` (default). See the [Text expansion](../overview.md#syntax) section below for details.

- **`basetime`** Set a start time for the count. Value is in microseconds. Only applied in the deprecated `strftime` expansion mode. To emulate in normal expansion mode use the `pts` function, supplying the start time (in seconds) as the second argument.

- **`fix_bounds`** If true, check and fix text coords to avoid clipping.

- **`fontcolor`** The color to be used for drawing fonts. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<fontcolor\> is "black".

- **`fontcolor_expr`** String which is expanded the same way as \<text\> to obtain dynamic \<fontcolor\> value. By default this option has empty value and is not processed. When this option is set, it overrides \<fontcolor\> option.

- **`font`** The font family to be used for drawing text. By default Sans.

- **`fontfile`** The font file to be used for drawing text. The path must be included. This parameter is mandatory if the fontconfig support is disabled.

- **`alpha`** Draw the text applying alpha blending. The value can be a number between 0.0 and 1.0. The expression accepts the same variables \<x, y\> as well. The default value is 1. Please see \<fontcolor_expr\>.

- **`fontsize`** The font size to be used for drawing text. The default value of \<fontsize\> is 16.

- **`text_shaping`** If set to 1, attempt to shape the text (for example, reverse the order of right-to-left text and join Arabic characters) before drawing it. Otherwise, just draw the text exactly as given. By default 1 (if supported).

- **`ft_load_flags`** The flags to be used for loading the fonts.

  The flags map the corresponding flags supported by libfreetype, and are a combination of the following values:

  - **\<default\>**

  - **\<no_scale\>**

  - **\<no_hinting\>**

  - **\<render\>**

  - **\<no_bitmap\>**

  - **\<vertical_layout\>**

  - **\<force_autohint\>**

  - **\<crop_bitmap\>**

  - **\<pedantic\>**

  - **\<ignore_global_advance_width\>**

  - **\<no_recurse\>**

  - **\<ignore_transform\>**

  - **\<monochrome\>**

  - **\<linear_design\>**

  - **\<no_autohint\>**

  Default value is "default".

  For more information consult the documentation for the FT_LOAD\_\* libfreetype flags.

- **`shadowcolor`** The color to be used for drawing a shadow behind the drawn text. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<shadowcolor\> is "black".

- **`boxw`** Set the width of the box to be drawn around text. The default value of \<boxw\> is computed automatically to match the text width

- **`boxh`** Set the height of the box to be drawn around text. The default value of \<boxh\> is computed automatically to match the text height

- **`shadowx`**

- **`shadowy`** The x and y offsets for the text shadow position with respect to the position of the text. They can be either positive or negative values. The default value for both is "0".

- **`start_number`** The starting frame number for the n/frame_num variable. The default value is "0".

- **`tabsize`** The size in number of spaces to use for rendering the tab. Default value is 4.

- **`timecode`** Set the initial timecode representation in "hh:mm:ss\[:;.\]ff" format. It can be used with or without text parameter. \<timecode_rate\> option must be specified.

- **`timecode_rate, rate, r`** Set the timecode frame rate (timecode only). Value will be rounded to nearest integer. Minimum value is "1". Drop-frame timecode is supported for frame rates 30 & 60.

- **`tc24hmax`** If set to 1, the output of the timecode option will wrap around at 24 hours. Default is 0 (disabled).

- **`text`** The text string to be drawn. The text must be a sequence of UTF-8 encoded characters. This parameter is mandatory if no file is specified with the parameter \<textfile\>.

- **`textfile`** A text file containing text to be drawn. The text must be a sequence of UTF-8 encoded characters.

  This parameter is mandatory if no text string is specified with the parameter \<text\>.

  If both \<text\> and \<textfile\> are specified, an error is thrown.

- **`text_source`** Text source should be set as side_data_detection_bboxes if you want to use text data in detection bboxes of side data.

  If text source is set, \<text\> and \<textfile\> will be ignored and still use text data in detection bboxes of side data. So please do not use this parameter if you are not sure about the text source.

- **`reload`** The \<textfile\> will be reloaded at specified frame interval. Be sure to update \<textfile\> atomically, or it may be read partially, or even fail. Range is 0 to INT_MAX. Default is 0.

- **`x`**

- **`y`** The expressions which specify the offsets where text will be drawn within the video frame. They are relative to the top/left border of the output image.

  The default value of \<x\> and \<y\> is "0".

  See below for the list of accepted constants and functions.

The parameters for \<x\> and \<y\> are expressions containing the following constants and functions:

- **`dar`** input display aspect ratio, it is the same as (\<w\> / \<h\>) \* \<sar\>

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`line_h, lh`** the height of each text line

- **`main_h, h, H`** the input height

- **`main_w, w, W`** the input width

- **`max_glyph_a, ascent`** the maximum distance from the baseline to the highest/upper grid coordinate used to place a glyph outline point, for all the rendered glyphs. It is a positive value, due to the grid's orientation with the Y axis upwards.

- **`max_glyph_d, descent`** the maximum distance from the baseline to the lowest grid coordinate used to place a glyph outline point, for all the rendered glyphs. This is a negative value, due to the grid's orientation, with the Y axis upwards.

- **`max_glyph_h`** maximum glyph height, that is the maximum height for all the glyphs contained in the rendered text, it is equivalent to \<ascent\> - \<descent\>.

- **`max_glyph_w`** maximum glyph width, that is the maximum width for all the glyphs contained in the rendered text

- **`font_a`** the ascent size defined in the font metrics

- **`font_d`** the descent size defined in the font metrics

- **`top_a`** the maximum ascender of the glyphs of the first text line

- **`bottom_d`** the maximum descender of the glyphs of the last text line

- **`n`** the number of input frame, starting from 0

- **`rand(min, max)`** return a random number included between \<min\> and \<max\>

- **`sar`** The input sample aspect ratio.

- **`t`** timestamp expressed in seconds, NAN if the input timestamp is unknown

- **`text_h, th`** the height of the rendered text

- **`text_w, tw`** the width of the rendered text

- **`x`**

- **`y`** the x and y offset coordinates where the text is drawn.

  These parameters allow the \<x\> and \<y\> expressions to refer to each other, so you can for example specify `y=x/dar`.

- **`pict_type`** A one character description of the current frame's picture type.

- **`pkt_pos`** The current packet's position in the input file or stream (in bytes, from the start of the input). A value of -1 indicates this info is not available.

- **`duration`** The current packet's duration, in seconds.

- **`pkt_size`** The current packet's size (in bytes).

## Text expansion

If `expansion` is set to `strftime`, the filter recognizes sequences accepted by the `strftime` C function in the provided text and expands them accordingly. Check the documentation of `strftime`. This feature is deprecated in favor of `normal` expansion with the `gmtime` or `localtime` expansion functions.

If `expansion` is set to `none`, the text is printed verbatim.

If `expansion` is set to `normal` (which is the default), the following expansion mechanism is used.

The backslash character `\`, followed by any character, always expands to the second character.

Sequences of the form `%{...}` are expanded. The text between the braces is a function name, possibly followed by arguments separated by ':'. If the arguments contain special characters or delimiters (':' or '}'), they should be escaped.

Note that they probably must also be escaped as the value for the `text` option in the filter argument string and as the filter argument in the filtergraph description, and possibly also for the shell, that makes up to four levels of escaping; using a text file with the `textfile` option avoids these problems.

The following functions are available:

- **`expr, e`** The expression evaluation result.

  It must take one argument specifying the expression to be evaluated, which accepts the same constants and functions as the \<x\> and \<y\> values. Note that not all constants should be used, for example the text size is not known when evaluating the expression, so the constants \<text_w\> and \<text_h\> will have an undefined value.

- **`expr_int_format, eif`** Evaluate the expression's value and output as formatted integer.

  The first argument is the expression to be evaluated, just as for the \<expr\> function. The second argument specifies the output format. Allowed values are `x`, `X`, `d` and `u`. They are treated exactly as in the `printf` function. The third parameter is optional and sets the number of positions taken by the output. It can be used to add padding with zeros from the left.

- **`gmtime`** The time at which the filter is running, expressed in UTC. It can accept an argument: a `strftime` C function format string. The format string is extended to support the variable \<%\[1-6\]N\> which prints fractions of the second with optionally specified number of digits.

- **`localtime`** The time at which the filter is running, expressed in the local time zone. It can accept an argument: a `strftime` C function format string. The format string is extended to support the variable \<%\[1-6\]N\> which prints fractions of the second with optionally specified number of digits.

- **`metadata`** Frame metadata. Takes one or two arguments.

  The first argument is mandatory and specifies the metadata key.

  The second argument is optional and specifies a default value, used when the metadata key is not found or empty.

  Available metadata can be identified by inspecting entries starting with TAG included within each frame section printed by running `ffprobe -show_frames`.

  String metadata generated in filters leading to the drawtext filter are also available.

- **`n, frame_num`** The frame number, starting from 0.

- **`pict_type`** A one character description of the current picture type.

- **`pts`** The timestamp of the current frame. It can take up to three arguments.

  The first argument is the format of the timestamp; it defaults to `flt` for seconds as a decimal number with microsecond accuracy; `hms` stands for a formatted \<\[-\]HH:MM:SS.mmm\> timestamp with millisecond accuracy. `gmtime` stands for the timestamp of the frame formatted as UTC time; `localtime` stands for the timestamp of the frame formatted as local time zone time.

  The second argument is an offset added to the timestamp.

  If the format is set to `hms`, a third argument `24HH` may be supplied to present the hour part of the formatted timestamp in 24h format (00-23).

  If the format is set to `localtime` or `gmtime`, a third argument may be supplied: a `strftime` C function format string. By default, \<YYYY-MM-DD HH:MM:SS\> format will be used.

## Commands

This filter supports altering parameters via commands:

- **`reinit`** Alter existing filter parameters.

  Syntax for the argument is the same as for filter invocation, e.g.

  ``` text
  fontsize=56:fontcolor=green:text='Hello World'
  ```

  Full filter invocation with sendcmd would look like this:

  ``` text
  sendcmd=c='56.0 drawtext reinit fontsize=56\:fontcolor=green\:text=Hello\\ World'
  ```

  If the entire argument can't be parsed or applied as valid values then the filter will continue with its existing parameters.

The following options are also supported as [commands](#commands):

- x

- y

- alpha

- fontsize

- fontcolor

- boxcolor

- bordercolor

- shadowcolor

- box

- boxw

- boxh

- boxborderw

- line_spacing

- text_align

- shadowx

- shadowy

- borderw

## Examples

- Draw "Test Text" with font FreeSerif, using the default values for the optional parameters.

  ``` text
  drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='Test Text'"
  ```

- Draw 'Test Text' with font FreeSerif of size 24 at position x=100 and y=50 (counting from the top-left corner of the screen), text is yellow with a red box around it. Both the text and the box have an opacity of 20%.

  ``` text
  drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='Test Text':\
            x=100: y=50: fontsize=24: fontcolor=yellow@0.2: box=1: boxcolor=red@0.2"
  ```

  Note that the double quotes are not necessary if spaces are not used within the parameter list.

- Show the text at the center of the video frame:

  ``` text
  drawtext="fontsize=30:fontfile=FreeSerif.ttf:text='hello world':x=(w-text_w)/2:y=(h-text_h)/2"
  ```

- Show the text at a random position, switching to a new position every 30 seconds:

  ``` text
  drawtext="fontsize=30:fontfile=FreeSerif.ttf:text='hello world':x=if(eq(mod(t\,30)\,0)\,rand(0\,(w-text_w))\,x):y=if(eq(mod(t\,30)\,0)\,rand(0\,(h-text_h))\,y)"
  ```

- Show a text line sliding from right to left in the last row of the video frame. The file `LONG_LINE` is assumed to contain a single line with no newlines.

  ``` text
  drawtext="fontsize=15:fontfile=FreeSerif.ttf:text=LONG_LINE:y=h-line_h:x=-50*t"
  ```

- Show the content of file `CREDITS` off the bottom of the frame and scroll up.

  ``` text
  drawtext="fontsize=20:fontfile=FreeSerif.ttf:textfile=CREDITS:y=h-20*t"
  ```

- Draw a single green letter "g", at the center of the input video. The glyph baseline is placed at half screen height.

  ``` text
  drawtext="fontsize=60:fontfile=FreeSerif.ttf:fontcolor=green:text=g:x=(w-max_glyph_w)/2:y=h/2-ascent"
  ```

- Show text for 1 second every 3 seconds:

  ``` text
  drawtext="fontfile=FreeSerif.ttf:fontcolor=white:x=100:y=x/dar:enable=lt(mod(t\,3)\,1):text='blink'"
  ```

- Use fontconfig to set the font. Note that the colons need to be escaped.

  ``` text
  drawtext='fontfile=Linux Libertine O-40\\:style=Semibold:text=FFmpeg'
  ```

- Draw "Test Text" with font size dependent on height of the video.

  ``` text
  drawtext="text='Test Text': fontsize=h/30: x=(w-text_w)/2: y=(h-text_h*2)"
  ```

- Print the date of a real-time encoding (see documentation for the `strftime` C function):

  ``` text
  drawtext='fontfile=FreeSans.ttf:text=%{localtime\:%a %b %d %Y}'
  ```

- Show text fading in and out (appearing/disappearing):

  ``` shell
  #!/bin/sh
  DS=1.0 # display start
  DE=10.0 # display end
  FID=1.5 # fade in duration
  FOD=5 # fade out duration
  ffplay -f lavfi "color,drawtext=text=TEST:fontsize=50:fontfile=FreeSerif.ttf:fontcolor_expr=ff0000%{eif\\\\: clip(255*(1*between(t\\, $DS + $FID\\, $DE - $FOD) + ((t - $DS)/$FID)*between(t\\, $DS\\, $DS + $FID) + (-(t - $DE)/$FOD)*between(t\\, $DE - $FOD\\, $DE) )\\, 0\\, 255) \\\\: x\\\\: 2 }"
  ```

- Horizontally align multiple separate texts. Note that `max_glyph_a` and the `fontsize` value are included in the `y` offset.

  ``` text
  drawtext=fontfile=FreeSans.ttf:text=DOG:fontsize=24:x=10:y=20+24-max_glyph_a,
  drawtext=fontfile=FreeSans.ttf:text=cow:fontsize=24:x=80:y=20+24-max_glyph_a
  ```

- Plot special \<lavf.image2dec.source_basename\> metadata onto each frame if such metadata exists. Otherwise, plot the string "NA". Note that image2 demuxer must have option `-export_path_metadata 1` for the special metadata fields to be available for filters.

  ``` text
  drawtext="fontsize=20:fontcolor=white:fontfile=FreeSans.ttf:text='%{metadata\:lavf.image2dec.source_basename\:NA}':x=10:y=10"
  ```

For more information about libfreetype, check: <http://www.freetype.org/>.

For more information about fontconfig, check: <http://freedesktop.org/software/fontconfig/fontconfig-user.html>.

For more information about libfribidi, check: <http://fribidi.org/>.

For more information about libharfbuzz, check: <https://github.com/harfbuzz/harfbuzz>.
