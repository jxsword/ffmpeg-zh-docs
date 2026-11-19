# scale

Scale (resize) the input video, using the libswscale library.

The scale filter forces the output display aspect ratio to be the same of the input, by changing the output sample aspect ratio.

If the input image format is different from the format requested by the next filter, the scale filter will convert the input to the requested format.

## Options

The filter accepts the following options, any of the options supported by the libswscale scaler, as well as any of the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

See section "the ffmpeg-scaler manual" in `ffmpeg-scaler` for the complete list of scaler options.

- **`width, w`**

- **`height, h`** Set the output video dimension expression. Default value is the input dimension.

  If the \<width\> or \<w\> value is 0, the input width is used for the output. If the \<height\> or \<h\> value is 0, the input height is used for the output.

  If one and only one of the values is -n with n \>= 1, the scale filter will use a value that maintains the aspect ratio of the input image, calculated from the other specified dimension. After that it will, however, make sure that the calculated dimension is divisible by n and adjust the value if necessary.

  If both values are -n with n \>= 1, the behavior will be identical to both values being set to 0 as previously detailed.

  See below for the list of accepted constants for use in the dimension expression.

- **`eval`** Specify when to evaluate \<width\> and \<height\> expression. It accepts the following values:

  - **`init`** Only evaluate expressions once during the filter initialization or when a command is processed.

  - **`frame`** Evaluate expressions for each incoming frame.

  Default value is `init`.

- **`interl`** Set the interlacing mode. It accepts the following values:

  - **`1`** Force interlaced aware scaling.

  - **`0`** Do not apply interlaced scaling.

  - **`-1`** Select interlaced aware scaling depending on whether the source frames are flagged as interlaced or not.

  Default value is `0`.

- **`flags`** Set libswscale scaling flags. See section "the ffmpeg-scaler manual" in `ffmpeg-scaler` for the complete list of values. If not explicitly specified the filter applies the default flags.

- **`param0, param1`** Set libswscale input parameters for scaling algorithms that need them. See section "the ffmpeg-scaler manual" in `ffmpeg-scaler` for the complete documentation. If not explicitly specified the filter applies empty parameters.

- **`intent`** Set the ICC rendering intent to use when transforming between different color spaces. It accepts the following values:

  - **`perceptual`** Use a perceptually guided tone and gamut mapping curve. The exact details of the mapping used may change at any time and should not be relied on as stable. This intent is recommended for final viewing of image/video content in typical viewing settings.

  - **`relative_colorimetric`** Statically clip out-of-gamut colors using a colorimetric clipping curve which attempts to find the colorimetrically least dissimilar in-gamut color. This intent performs white point adaptation and black point adaptation. This is the default. This intent is recommended wherever faithful color reproduction is of the utmost importance, even at the cost of clipping.

  - **`absolute_colorimetric`** Hard clip out-of-gamut colors with no attempt at white or black point reproduction. This intent will reproduce in-gamut colors 1:1 on the output display as they would appear on the reference display, assuming the output display is appropriately calibrated.

  - **`saturation`** Performs saturation mapping - that is, stretches the input color volume directly onto the output color volume, in non-linear fashion that preserves the original signal appearance as much as possible. This intent is recommended for signal content evaluation, as it will not lead to any clipping. It is roughly analogous to not performing any color mapping, although it still takes into account the mastering display primaries and any differences in encoding TRC.

- **`size, s`** Set the video size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`in_color_matrix`**

- **`out_color_matrix`** Set in/output YCbCr color space type.

  This allows the autodetected value to be overridden as well as allows forcing a specific value used for the output and encoder.

  If not specified, the color space type depends on the pixel format.

  Possible values:

  - **`auto`** Choose automatically.

  - **`bt709`** Format conforming to International Telecommunication Union (ITU) Recommendation BT.709.

  - **`fcc`** Set color space conforming to the United States Federal Communications Commission (FCC) Code of Federal Regulations (CFR) Title 47 (2003) 73.682 (a).

  - **`bt601`**

  - **`bt470`**

  - **`smpte170m`** Set color space conforming to:

    - ITU Radiocommunication Sector (ITU-R) Recommendation BT.601

    - ITU-R Rec. BT.470-6 (1998) Systems B, B1, and G

    - Society of Motion Picture and Television Engineers (SMPTE) ST 170:2004

  - **`smpte240m`** Set color space conforming to SMPTE ST 240:1999.

  - **`bt2020`** Set color space conforming to ITU-R BT.2020 non-constant luminance system.

- **`in_range`**

- **`out_range`** Set in/output YCbCr sample range.

  This allows the autodetected value to be overridden as well as allows forcing a specific value used for the output and encoder. If not specified, the range depends on the pixel format. Possible values:

  | Term                | Description                                      |
  |---------------------|--------------------------------------------------|
  | `auto/unknown`    | Choose automatically.                            |
  | `jpeg/full/pc`    | Set full range (0-255 in case of 8-bit luma).    |
  | `mpeg/limited/tv` | Set "MPEG" range (16-235 in case of 8-bit luma). |

- **`in_chroma_loc`**

- **`out_chroma_loc`** Set in/output chroma sample location. If not specified, center-sited chroma is used by default. Possible values:

  - **`auto, unknown`**

  - **`left`**

  - **`center`**

  - **`topleft`**

  - **`top`**

  - **`bottomleft`**

  - **`bottom`**

- **`in_primaries`**

- **`out_primaries`** Set in/output RGB primaries.

  This allows the autodetected value to be overridden as well as allows forcing a specific value used for the output and encoder. Possible values:

  - **`auto`** Choose automatically. This is the default.

  - **`bt709`**

  - **`bt470m`**

  - **`bt470bg`**

  - **`smpte170m`**

  - **`smpte240m`**

  - **`film`**

  - **`bt2020`**

  - **`smpte428`**

  - **`smpte431`**

  - **`smpte432`**

  - **`jedec-p22`**

  - **`ebu3213`**

- **`in_transfer`**

- **`out_transfer`** Set in/output transfer response curve (TRC).

  This allows the autodetected value to be overridden as well as allows forcing a specific value used for the output and encoder. Possible values:

  - **`auto`** Choose automatically. This is the default.

  - **`bt709`**

  - **`bt470m`**

  - **`gamma22`**

  - **`bt470bg`**

  - **`gamma28`**

  - **`smpte170m`**

  - **`smpte240m`**

  - **`linear`**

  - **`iec61966-2-1`**

  - **`srgb`**

  - **`iec61966-2-4`**

  - **`xvycc`**

  - **`bt1361e`**

  - **`bt2020-10`**

  - **`bt2020-12`**

  - **`smpte2084`**

  - **`smpte428`**

  - **`arib-std-b67`**

- **`force_original_aspect_ratio`** Enable decreasing or increasing output video width or height if necessary to keep the original aspect ratio. Possible values:

  | Term | Description |
  |----|----|
  | `disable` | Scale the video as specified and disable this feature. |
  | `decrease` | The output video dimensions will automatically be decreased if needed. |
  | `increase` | The output video dimensions will automatically be increased if needed. |

  One useful instance of this option is that when you know a specific device's maximum allowed resolution, you can use this to limit the output video to that, while retaining the aspect ratio. For example, device A allows 1280x720 playback, and your video is 1920x800. Using this option (set it to decrease) and specifying 1280x720 to the command line makes the output 1280x533.

  Please note that this is a different thing than specifying -1 for `w` or `h`, you still need to specify the output resolution for this option to work.

- **`force_divisible_by`** Ensures that both the output dimensions, width and height, are divisible by the given integer when used together with `force_original_aspect_ratio`. This works similar to using `-n` in the `w` and `h` options.

  This option respects the value set for `force_original_aspect_ratio`, increasing or decreasing the resolution accordingly. The video's aspect ratio may be slightly modified.

  This option can be handy if you need to have a video fit within or exceed a defined resolution using `force_original_aspect_ratio` but also have encoder restrictions on width or height divisibility.

- **`reset_sar`** Enabling this option leads to the output SAR being reset to 1. Additionally, if the user requests proportional scaling either through the width or height expressions, e.g. `w=-4:h=360` or `w=iw/2:h=-1` or by enabling `force_original_aspect_ratio`, then the input DAR is taken into account and the output is scaled to produce square pixels. Default is false.

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

- **\<n\>** The (sequential) number of the input frame, starting from 0. Only available with `eval=frame`.

- **\<t\>** The presentation timestamp of the input frame, expressed as a number of seconds. Only available with `eval=frame`.

- **\<pos\>** The position (byte offset) of the frame in the input stream, or NaN if this information is unavailable and/or meaningless (for example in case of synthetic video). Only available with `eval=frame`. Deprecated, do not use.

- **\<ref_w, rw\>**

- **\<ref_h, rh\>**

- **\<ref_a\>**

- **\<ref_dar, rdar\>**

- **\<ref_n\>**

- **\<ref_t\>**

- **\<ref_pos\>** Eqvuialent to the above, but for a second reference input. If any of these variables are present, this filter accepts two inputs.

## Examples

- Scale the input video to a size of 200x100

  ``` text
  scale=w=200:h=100
  ```

  This is equivalent to:

  ``` text
  scale=200:100
  ```

  or:

  ``` text
  scale=200x100
  ```

- Specify a size abbreviation for the output size:

  ``` text
  scale=qcif
  ```

  which can also be written as:

  ``` text
  scale=size=qcif
  ```

- Scale the input to 2x:

  ``` text
  scale=w=2*iw:h=2*ih
  ```

- The above is the same as:

  ``` text
  scale=2*in_w:2*in_h
  ```

- Scale the input to 2x with forced interlaced scaling:

  ``` text
  scale=2*iw:2*ih:interl=1
  ```

- Scale the input to half size:

  ``` text
  scale=w=iw/2:h=ih/2
  ```

- Increase the width, and set the height to the same size:

  ``` text
  scale=3/2*iw:ow
  ```

- Seek Greek harmony:

  ``` text
  scale=iw:1/PHI*iw
  scale=ih*PHI:ih
  ```

- Increase the height, and set the width to 3/2 of the height:

  ``` text
  scale=w=3/2*oh:h=3/5*ih
  ```

- Increase the size, making the size a multiple of the chroma subsample values:

  ``` text
  scale="trunc(3/2*iw/hsub)*hsub:trunc(3/2*ih/vsub)*vsub"
  ```

- Increase the width to a maximum of 500 pixels, keeping the same aspect ratio as the input:

  ``` text
  scale=w='min(500\, iw*3/2):h=-1'
  ```

- Make pixels square by combining scale and setsar:

  ``` text
  scale='trunc(ih*dar):ih',setsar=1/1
  ```

- Make pixels square using reset_sar, making sure the resulting resolution is even (required by some codecs):

  ``` text
  scale='-2:ih-mod(ih,2):reset_sar=1'
  ```

- Scale to target exactly, however reset SAR to 1:

  ``` text
  scale='400:300:reset_sar=1'
  ```

- Scale to even dimensions that fit within 400x300, preserving input SAR:

  ``` text
  scale='400:300:force_original_aspect_ratio=decrease:force_divisible_by=2'
  ```

- Scale to produce square pixels with even dimensions that fit within 400x300:

  ``` text
  scale='400:300:force_original_aspect_ratio=decrease:force_divisible_by=2:reset_sar=1'
  ```

- Scale a subtitle stream (sub) to match the main video (main) in size before overlaying. ("scale2ref")

  ``` text
  '[main]split[a][b]; [ref][a]scale=rw:rh[c]; [b][c]overlay'
  ```

- Scale a logo to 1/10th the height of a video, while preserving its display aspect ratio.

  ``` text
  [logo-in][video-in]scale=w=oh*dar:h=rh/10[logo-out]
  ```

## Commands

This filter supports the following commands:

- **`width, w`**

- **`height, h`** Set the output video dimension expression. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
