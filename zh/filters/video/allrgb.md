# allrgb, allyuv, color, colorchart, colorspectrum, haldclutsrc, nullsrc, pal75bars, pal100bars, rgbtestsrc, smptebars, smptehdbars, testsrc, testsrc2, yuvtestsrc

The `allrgb` source returns frames of size 4096x4096 of all rgb colors.

The `allyuv` source returns frames of size 4096x4096 of all yuv colors.

The `color` source provides an uniformly colored input.

The `colorchart` source provides a colors checker chart.

The `colorspectrum` source provides a color spectrum input.

The `haldclutsrc` source provides an identity Hald CLUT. See also [haldclut](haldclut.md#haldclut) filter.

The `nullsrc` source returns unprocessed video frames. It is mainly useful to be employed in analysis / debugging tools, or as the source for filters which ignore the input data.

The `pal75bars` source generates a color bars pattern, based on EBU PAL recommendations with 75% color levels.

The `pal100bars` source generates a color bars pattern, based on EBU PAL recommendations with 100% color levels.

The `rgbtestsrc` source generates an RGB test pattern useful for detecting RGB vs BGR issues. You should see a red, green and blue stripe from top to bottom.

The `smptebars` source generates a color bars pattern, based on the SMPTE Engineering Guideline EG 1-1990.

The `smptehdbars` source generates a color bars pattern, based on the SMPTE RP 219-2002.

The `testsrc` source generates a test video pattern, showing a color pattern, a scrolling gradient and a timestamp. This is mainly intended for testing purposes.

The `testsrc2` source is similar to testsrc, but supports more pixel formats instead of just `rgb24`. This allows using it as an input for other tests without requiring a format conversion.

The `yuvtestsrc` source generates an YUV test pattern. You should see a y, cb and cr stripe from top to bottom.

The sources accept the following parameters:

- **`level`** Specify the level of the Hald CLUT, only available in the `haldclutsrc` source. A level of `N` generates a picture of `N*N*N` by `N*N*N` pixels to be used as identity matrix for 3D lookup tables. Each component is coded on a `1/(N*N)` scale.

- **`color, c`** Specify the color of the source, only available in the `color` source. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`size, s`** Specify the size of the sourced video. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. The default value is `320x240`.

  This option is not available with the `allrgb`, `allyuv`, and `haldclutsrc` filters.

- **`rate, r`** Specify the frame rate of the sourced video, as the number of frames generated per second. It has to be a string in the format \<frame_rate_num\>/\<frame_rate_den\>, an integer number, a floating point number or a valid video frame rate abbreviation. The default value is "25".

- **`duration, d`** Set the duration of the sourced video. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

  If not specified, or the expressed duration is negative, the video is supposed to be generated forever.

  Since the frame rate is used as time base, all frames including the last one will have their full duration. If the specified duration is not a multiple of the frame duration, it will be rounded up.

- **`sar`** Set the sample aspect ratio of the sourced video.

- **`alpha`** Specify the alpha (opacity) of the background, only available in the `testsrc2` source. The value must be between 0 (fully transparent) and 255 (fully opaque, the default).

- **`decimals, n`** Set the number of decimals to show in the timestamp, only available in the `testsrc` source.

  The displayed timestamp value will correspond to the original timestamp value multiplied by the power of 10 of the specified value. Default value is 0.

- **`type`** Set the type of the color spectrum, only available in the `colorspectrum` source. Can be one of the following:

  - **`black`**

  - **`white`**

  - **`all`**

- **`patch_size`** Set patch size of single color patch, only available in the `colorchart` source. Default is `64x64`.

- **`preset`** Set colorchecker colors preset, only available in the `colorchart` source.

  Available values are:

  - **`reference`**

  - **`skintones`**

  Default value is `reference`.

## Examples

- Generate a video with a duration of 5.3 seconds, with size 176x144 and a frame rate of 10 frames per second:

  ``` text
  testsrc=duration=5.3:size=qcif:rate=10
  ```

- The following graph description will generate a red source with an opacity of 0.2, with size "qcif" and a frame rate of 10 frames per second:

  ``` text
  color=c=red@0.2:s=qcif:r=10
  ```

- If the input content is to be ignored, `nullsrc` can be used. The following command generates noise in the luma plane by employing the `geq` filter:

  ``` text
  nullsrc=s=256x256, geq=random(1)*255:128:128
  ```

## Commands

The `color` source supports the following commands:

- **`c, color`** Set the color of the created image. Accepts the same syntax of the corresponding `color` option.
