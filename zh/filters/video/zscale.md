# zscale

Scale (resize) the input video, using the z.lib library: <https://github.com/sekrit-twc/zimg>. To enable compilation of this filter, you need to configure FFmpeg with `--enable-libzimg`.

The zscale filter forces the output display aspect ratio to be the same as the input, by changing the output sample aspect ratio.

If the input image format is different from the format requested by the next filter, the zscale filter will convert the input to the requested format.

## Options

The filter accepts the following options.

- **`width, w`**

- **`height, h`** Set the output video dimension expression. Default value is the input dimension.

  If the \<width\> or \<w\> value is 0, the input width is used for the output. If the \<height\> or \<h\> value is 0, the input height is used for the output.

  If one and only one of the values is -n with n \>= 1, the zscale filter will use a value that maintains the aspect ratio of the input image, calculated from the other specified dimension. After that it will, however, make sure that the calculated dimension is divisible by n and adjust the value if necessary.

  If both values are -n with n \>= 1, the behavior will be identical to both values being set to 0 as previously detailed.

  See below for the list of accepted constants for use in the dimension expression.

- **`size, s`** Set the video size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`dither, d`** Set the dither type.

  Possible values are:

  - **\<none\>**

  - **\<ordered\>**

  - **\<random\>**

  - **\<error_diffusion\>**

  Default is none.

- **`filter, f`** Set the resize filter type.

  Possible values are:

  - **\<point\>**

  - **\<bilinear\>**

  - **\<bicubic\>**

  - **\<spline16\>**

  - **\<spline36\>**

  - **\<spline64\>**

  - **\<lanczos\>**

  Default is bilinear.

- **`range, r`** Set the color range.

  Possible values are:

  - **\<input\>**

  - **\<limited\>**

  - **\<full\>**

  Default is same as input.

- **`primaries, p`** Set the color primaries.

  Possible values are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<170m\>**

  - **\<240m\>**

  - **\<2020\>**

  Default is same as input.

- **`transfer, t`** Set the transfer characteristics.

  Possible values are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<601\>**

  - **\<linear\>**

  - **\<2020_10\>**

  - **\<2020_12\>**

  - **\<smpte2084\>**

  - **\<iec61966-2-1\>**

  - **\<arib-std-b67\>**

  Default is same as input.

- **`matrix, m`** Set the colorspace matrix.

  Possible value are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<470bg\>**

  - **\<170m\>**

  - **\<2020_ncl\>**

  - **\<2020_cl\>**

  Default is same as input.

- **`rangein, rin`** Set the input color range.

  Possible values are:

  - **\<input\>**

  - **\<limited\>**

  - **\<full\>**

  Default is same as input.

- **`primariesin, pin`** Set the input color primaries.

  Possible values are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<170m\>**

  - **\<240m\>**

  - **\<2020\>**

  Default is same as input.

- **`transferin, tin`** Set the input transfer characteristics.

  Possible values are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<601\>**

  - **\<linear\>**

  - **\<2020_10\>**

  - **\<2020_12\>**

  Default is same as input.

- **`matrixin, min`** Set the input colorspace matrix.

  Possible value are:

  - **\<input\>**

  - **\<709\>**

  - **\<unspecified\>**

  - **\<470bg\>**

  - **\<170m\>**

  - **\<2020_ncl\>**

  - **\<2020_cl\>**

- **`chromal, c`** Set the output chroma location.

  Possible values are:

  - **\<input\>**

  - **\<left\>**

  - **\<center\>**

  - **\<topleft\>**

  - **\<top\>**

  - **\<bottomleft\>**

  - **\<bottom\>**

- **`chromalin, cin`** Set the input chroma location.

  Possible values are:

  - **\<input\>**

  - **\<left\>**

  - **\<center\>**

  - **\<topleft\>**

  - **\<top\>**

  - **\<bottomleft\>**

  - **\<bottom\>**

- **`npl`** Set the nominal peak luminance.

- **`param_a`** Parameter A for scaling filters. Parameter "b" for bicubic, and the number of filter taps for lanczos.

- **`param_b`** Parameter B for scaling filters. Parameter "c" for bicubic.

The values of the `w` and `h` options are expressions containing the following constants:

- **\<in_w\>**

- **\<in_h\>** The input width and height

- **\<iw\>**

- **\<ih\>** These are the same as \<in_w\> and \<in_h\>.

- **\<out_w\>**

- **\<out_h\>** The output (scaled) width and height

- **\<ow\>**

- **\<oh\>** These are the same as \<out_w\> and \<out_h\>

- **\<a\>** The same as \<iw\> / \<ih\>

- **\<sar\>** input sample aspect ratio

- **\<dar\>** The input display aspect ratio. Calculated from `(iw / ih) * sar`.

- **\<hsub\>**

- **\<vsub\>** horizontal and vertical input chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **\<ohsub\>**

- **\<ovsub\>** horizontal and vertical output chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

## Commands

This filter supports the following commands:

- **`width, w`**

- **`height, h`** Set the output video dimension expression. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
