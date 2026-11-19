# libplacebo

Flexible GPU-accelerated processing filter based on libplacebo (<https://code.videolan.org/videolan/libplacebo>).

## Options

The options for this filter are divided into the following sections:

### Output mode

These options control the overall output mode. By default, libplacebo will try to preserve the source colorimetry and size as best as it can, but it will apply any embedded film grain, dolby vision metadata or anamorphic SAR present in source frames.

- **`inputs`** Set the number of inputs. This can be used, alongside the `idx` variable, to allow placing/blending multiple inputs inside the output frame. This effectively enables functionality similar to [hstack](hstack.md#hstack), [overlay](overlay.md#overlay), etc.

- **`w`**

- **`h`** Set the output video dimension expression. Default values are `iw` and `ih`.

  Allows for the same expressions as the [scale](scale.md#scale) filter.

- **`crop_x`**

- **`crop_y`** Set the input crop x/y expressions, default values are `(iw-cw)/2` and `(ih-ch)/2`.

- **`crop_w`**

- **`crop_h`** Set the input crop width/height expressions, default values are `iw` and `ih`.

- **`pos_x`**

- **`pos_y`** Set the output placement x/y expressions, default values are `(ow-pw)/2` and `(oh-ph)/2`.

- **`pos_w`**

- **`pos_h`** Set the output placement width/height expressions, default values are `ow` and `oh`.

- **`rotate`** Rotate the input frame clockwise by the specified angle.

  - **`0, 360`**

  - **`90`**

  - **`180`**

  - **`270`**

- **`fps`** Set the output frame rate. This can be rational, e.g. `60000/1001`. If set to the special string `none` (the default), input timestamps will instead be passed through to the output unmodified. Otherwise, the input video frames will be interpolated as necessary to rescale the video to the specified target framerate, in a manner as determined by the `frame_mixer` option.

- **`format`** Set the output format override. If unset (the default), frames will be output in the same format as the respective input frames. Otherwise, format conversion will be performed.

- **`force_original_aspect_ratio`**

- **`force_divisible_by`** Work the same as the identical [scale](scale.md#scale) filter options. Note that `force_divisible_by` also works with `fit_sense=constraint`.

- **`reset_sar`** If enabled, output frames will always have a pixel aspect ratio of 1:1. If disabled (the default), any aspect ratio mismatches, including those from e.g. anamorphic video sources, are forwarded to the output pixel aspect ratio.

- **`normalize_sar`** Like `reset_sar`, but instead of stretching the video content to fill the new output aspect ratio, the content is instead padded or cropped as necessary. Mutually exclusive with `fit_mode`. Disabled by default.

- **`pad_crop_ratio`** Specifies a ratio (between `0.0` and `1.0`) between padding and cropping when the input aspect ratio does not match the output aspect ratio and `normalize_sar` is in effect. The default of `0.0` always pads the content with black borders, while a value of `1.0` always crops off parts of the content. Intermediate values are possible, leading to a mix of the two approaches.

- **`fit_mode`** Specify the content fit strategy according to a list of predefined modes. Determines how the input image is to be placed inside the destination crop rectangle (as defined by `pos_x/y` and `pos_w/h`). The names and their implementations are taken from the CSS 'object-fit' property. Note that this option is mutually exclusive with `normalize_sar`. Defaults to `fill`. Valid values are:

  - **`fill`** Stretch the input to the output rectangle, ignoring aspect ratio mismatches. Note that unless `reset_sar` is also enabled, the output will still have the correct pixel aspect ratio tagged.

  - **`contain`** Scale the input to fit inside the output, preserving aspect ratio by padding. Equivalent to `normalize_sar` with `pad_crop_ratio` set to `0.0`.

  - **`cover`** Scale the input to fill the output, preserving aspect ratio by cropping. Equivalent to `normalize_sar` with `pad_crop_ratio` set to `1.0`.

  - **`none, place`** Don't scale the input. The input will be placed inside the output rectangle at its natural size; which may result in additional padding or cropping.

  - **`scale_down`** Scale the input down as much as needed to fit inside the output. Equivalent to either `contain` or `none`, depending on whether the input is larger than the output or not.

- **`fit_sense`** When `fit_mode` is in use, this option controls how the fit strategy is applied against the specified output resolution. Mutually exclusive with `force_original_aspect_ratio`. Valid values are:

  - **`target`** The computed output resolution is taken as the exact size of the output frame. This is the default behavior.

  - **`constraint`** The computed output resolution is a size reference against which the fit mode is applied, enlarging or decreasing the true frame size as needed to fit the content.

- **`fillcolor`** Set the color used to fill the output area not covered by the output image, for example as a result of `normalize_sar`. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Defaults to `black@0`.

- **`corner_rounding`** Render frames with rounded corners. The value, given as a float ranging from `0.0` to `1.0`, indicates the relative degree of rounding, from fully square to fully circular. In other words, it gives the radius divided by half the smaller side length. Defaults to `0.0`.

- **`lut`** Specifies a custom LUT (in Adobe .cube format) to apply to the colors as part of color conversion. The exact interpretation depends on the value of `lut_type`.

- **`lut_type`** Controls the interpretation of color values fed to and from the LUT specified as `lut`. Valid values are:

  - **`auto`** Chooses the interpretation of the LUT automatically from tagged metadata, and otherwise falls back to `native`. (Default)

  - **`native`** Applied to raw image contents in its native RGB colorspace (non-linear light), before conversion to the output color space.

  - **`normalized`** Applied to the normalized RGB image contents, in linear light, before conversion to the output color space.

  - **`conversion`** Fully replaces the conversion from the image color space to the output color space. If such a LUT is present, it has the highest priority, and overrides any ICC profiles, as well as options related to tone mapping and output colorimetry (`color_primaries`, `color_trc`).

- **`extra_opts`** Pass extra libplacebo internal configuration options. These can be specified as a list of \<key\>=\<value\> pairs separated by ':'. The following example shows how to configure a custom filter kernel ("EWA LanczosSharp") and use it to double the input image resolution:

  ``` text
  -vf "libplacebo=w=iw*2:h=ih*2:extra_opts='upscaler=custom\:upscaler_preset=ewa_lanczos\:upscaler_blur=0.9812505644269356'"
  ```

- **`shader_cache`** File path of a cache directory that libplacebo will use to store and load cached shader objects. This cache is not cleaned up automatically. If the path does not end in a directory separator, the generated filenames will be effectively prefixed by the last path component. All directories must already exist.

  ``` text
  -vf "libplacebo=shader_cache=/tmp/pl-shader-"
  ```

- **`colorspace`**

- **`color_primaries`**

- **`color_trc`**

- **`range`**

- **`chroma_location`** Configure the colorspace that output frames will be delivered in. The default value of `auto` outputs frames in the same format as the input frames, leading to no change. For any other value, conversion will be performed.

  See the [setparams](setparams.md#setparams) filter for a list of possible values.

- **`alpha_mode`** Choose the desired output alpha mode, when the output format has an alpha channel. See the [setparams](setparams.md#setparams) filter for a list of possible values.

- **`apply_filmgrain`** Apply film grain (e.g. AV1 or H.274) if present in source frames, and strip it from the output. Enabled by default.

- **`apply_dolbyvision`** Apply Dolby Vision RPU metadata if present in source frames, and strip it from the output. Enabled by default. Note that Dolby Vision will always output BT.2020+PQ, overriding the usual input frame metadata. These will also be picked as the values of `auto` for the respective frame output options.

In addition to the expression constants documented for the [scale](scale.md#scale) filter, the `crop_w`, `crop_h`, `crop_x`, `crop_y`, `pos_w`, `pos_h`, `pos_x` and `pos_y` options can also contain the following constants:

- **`in_idx, idx`** The (0-based) numeric index of the currently active input stream.

- **`crop_w, cw`**

- **`crop_h, ch`** The computed values of `crop_w` and `crop_h`.

- **`pos_w, pw`**

- **`pos_h, ph`** The computed values of `pos_w` and `pos_h`.

- **`in_t, t`** The input frame timestamp, in seconds. NAN if input timestamp is unknown.

- **`out_t, ot`** The input frame timestamp, in seconds. NAN if input timestamp is unknown.

- **`n`** The input frame number, starting with 0.

### Scaling

The options in this section control how libplacebo performs upscaling and (if necessary) downscaling. Note that libplacebo will always internally operate on 4:4:4 content, so any sub-sampled chroma formats such as `yuv420p` will necessarily be upsampled and downsampled as part of the rendering process. That means scaling might be in effect even if the source and destination resolution are the same.

- **`upscaler`**

- **`downscaler`** Configure the filter kernel used for upscaling and downscaling. The respective defaults are `spline36` and `mitchell`. For a full list of possible values, pass `help` to these options. The most important values are:

  - **`none`** Forces the use of built-in GPU texture sampling (typically bilinear). Extremely fast but poor quality, especially when downscaling.

  - **`bilinear`** Bilinear interpolation. Can generally be done for free on GPUs, except when doing so would lead to aliasing. Fast and low quality.

  - **`nearest`** Nearest-neighbour interpolation. Sharp but highly aliasing.

  - **`oversample`** Algorithm that looks visually similar to nearest-neighbour interpolation but tries to preserve pixel aspect ratio. Good for pixel art, since it results in minimal distortion of the artistic appearance.

  - **`lanczos`** Standard sinc-sinc interpolation kernel.

  - **`spline36`** Cubic spline approximation of lanczos. No difference in performance, but has very slightly less ringing.

  - **`ewa_lanczos`** Elliptically weighted average version of lanczos, based on a jinc-jinc kernel. This is also popularly referred to as just "Jinc scaling". Slow but very high quality.

  - **`gaussian`** Gaussian kernel. Has certain ideal mathematical properties, but subjectively very blurry.

  - **`mitchell`** Cubic BC spline with parameters recommended by Mitchell and Netravali. Very little ringing.

- **`frame_mixer`** Controls the kernel used for mixing frames temporally. The default value is `none`, which disables frame mixing. For a full list of possible values, pass `help` to this option. The most important values are:

  - **`none`** Disables frame mixing, giving a result equivalent to "nearest neighbour" semantics.

  - **`oversample`** Oversamples the input video to create a "Smooth Motion"-type effect: if an output frame would exactly fall on the transition between two video frames, it is blended according to the relative overlap. This is the recommended option whenever preserving the original subjective appearance is desired.

  - **`mitchell_clamp`** Larger filter kernel that smoothly interpolates multiple frames in a manner designed to eliminate ringing and other artefacts as much as possible. This is the recommended option wherever maximum visual smoothness is desired.

  - **`linear`** Linear blend/fade between frames. Especially useful for constructing e.g. slideshows.

- **`antiringing`** Enables anti-ringing (for non-EWA filters). The value (between `0.0` and `1.0`) configures the strength of the anti-ringing algorithm. May increase aliasing if set too high. Disabled by default.

- **`sigmoid`** Enable sigmoidal compression during upscaling. Reduces ringing slightly. Enabled by default.

### Deinterlacing

Deinterlacing is automatically supported when frames are tagged as interlaced, however frames are not deinterlaced unless a deinterlacing algorithm is chosen.

- **`deinterlace`** The the deinterlacing algorithm to use.

  - **`weave`** No deinterlacing, weave fields together into a single frame. This is the default.

  - **`bob`** Naive bob deinterlacing, simply repeat each field line twice.

  - **`yadif`** Yet another deinterlacing filter. See the [yadif](yadif.md#yadif) filter for more details.

  - **`bwdif`** Bob weaver deinterlacing filter. See the [bwdif](bwdif.md#bwdif) filter for more details.

- **`skip_spatial_check`** Skip the spatial deinterlacing check when using `yadif` deinterlacing.

- **`send_fields`** Output a frame for each field, rather than for each frame. Note that this will always double the tagged output frame rate, even if the input does not contain any interlaced frames. Disabled by default.

### Debanding

Libplacebo comes with a built-in debanding filter that is good at counteracting many common sources of banding and blocking. Turning this on is highly recommended whenever quality is desired.

- **`deband`** Enable (fast) debanding algorithm. Disabled by default.

- **`deband_iterations`** Number of deband iterations of the debanding algorithm. Each iteration is performed with progressively increased radius (and diminished threshold). Recommended values are in the range `1` to `4`. Defaults to `1`.

- **`deband_threshold`** Debanding filter strength. Higher numbers lead to more aggressive debanding. Defaults to `4.0`.

- **`deband_radius`** Debanding filter radius. A higher radius is better for slow gradients, while a lower radius is better for steep gradients. Defaults to `16.0`.

- **`deband_grain`** Amount of extra output grain to add. Helps hide imperfections. Defaults to `6.0`.

### Color adjustment

A collection of subjective color controls. Not very rigorous, so the exact effect will vary somewhat depending on the input primaries and colorspace.

- **`brightness`** Brightness boost, between `-1.0` and `1.0`. Defaults to `0.0`.

- **`contrast`** Contrast gain, between `0.0` and `16.0`. Defaults to `1.0`.

- **`saturation`** Saturation gain, between `0.0` and `16.0`. Defaults to `1.0`.

- **`hue`** Hue shift in radians, between `-3.14` and `3.14`. Defaults to `0.0`. This will rotate the UV subvector, defaulting to BT.709 coefficients for RGB inputs.

- **`gamma`** Gamma adjustment, between `0.0` and `16.0`. Defaults to `1.0`.

- **`temperature`** Color temperature adjustment. Lower values make the output warmer/redder, down to `1667`, while higher values make the output cooler/bluer, up to `25000`. Defaults to `6500` (neutral white).

- **`cones`** Cone model to use for color blindness simulation. Accepts any combination of `l`, `m` and `s`. Here are some examples:

  | Term | Description |
  |----|----|
  | `m` | Deuteranomaly / deuteranopia (affecting 3%-4% of the population) |
  | `l` | Protanomaly / protanopia (affecting 1%-2% of the population) |
  | `l+m` | Monochromacy (very rare) |
  | `l+m+s` | Achromatopsy (complete loss of daytime vision, extremely rare) |

- **`cone-strength`** Gain factor for the cones specified by `cones`, between `0.0` and `10.0`. A value of `1.0` results in no change to color vision. A value of `0.0` (the default) simulates complete loss of those cones. Values above `1.0` result in exaggerating the differences between cones, which may help compensate for reduced color vision.

### Peak detection

To help deal with sources that only have static HDR10 metadata (or no tagging whatsoever), libplacebo uses its own internal frame analysis compute shader to analyze source frames and adapt the tone mapping function in realtime. If this is too slow, or if exactly reproducible frame-perfect results are needed, it's recommended to turn this feature off.

- **`peak_detect`** Enable HDR peak detection. Ignores static MaxCLL/MaxFALL values in favor of dynamic detection from the input. Note that the detected values do not get written back to the output frames, they merely guide the internal tone mapping process. Enabled by default.

- **`smoothing_period`** Peak detection smoothing period, between `0.0` and `1000.0`. Higher values result in peak detection becoming less responsive to changes in the input. Defaults to `20.0`.

- **`scene_threshold_low`**

- **`scene_threshold_high`** Lower and upper thresholds for scene change detection. Expressed in a logarithmic scale between `0.0` and `100.0`. Default to `1.0` and `3.0`, respectively. Setting either to a negative value disables this functionality.

- **`percentile`** Which percentile of the frame brightness histogram to use as the source peak for tone-mapping. Defaults to `99.995`, a fairly conservative value. Setting this to `100.0` disables frame histogram measurement and instead uses the true peak brightness for tone-mapping.

### Tone mapping

The options in this section control how libplacebo performs tone-mapping and gamut-mapping when dealing with mismatches between wide-gamut or HDR content. In general, libplacebo relies on accurate source tagging and mastering display gamut information to produce the best results.

- **`gamut_mode`** How to handle out-of-gamut colors that can occur as a result of colorimetric gamut mapping.

  - **`clip`** Do nothing, simply clip out-of-range colors to the RGB volume. Low quality but extremely fast.

  - **`perceptual`** Perceptually soft-clip colors to the gamut volume. This is the default.

  - **`relative`** Relative colorimetric hard-clip. Similar to `perceptual` but without the soft knee.

  - **`saturation`** Saturation mapping, maps primaries directly to primaries in RGB space. Not recommended except for artificial computer graphics for which a bright, saturated display is desired.

  - **`absolute`** Absolute colorimetric hard-clip. Performs no adjustment of the white point.

  - **`desaturate`** Hard-desaturates out-of-gamut colors towards white, while preserving the luminance. Has a tendency to distort the visual appearance of bright objects.

  - **`darken`** Linearly reduces content brightness to preserves saturated details, followed by clipping the remaining out-of-gamut colors.

  - **`warn`** Highlight out-of-gamut pixels (by inverting/marking them).

  - **`linear`** Linearly reduces chromaticity of the entire image to make it fit within the target color volume. Be careful when using this on BT.2020 sources without proper mastering metadata, as doing so will lead to excessive desaturation.

- **`tonemapping`** Tone-mapping algorithm to use. Available values are:

  - **`auto`** Automatic selection based on internal heuristics. This is the default.

  - **`clip`** Performs no tone-mapping, just clips out-of-range colors. Retains perfect color accuracy for in-range colors but completely destroys out-of-range information. Does not perform any black point adaptation. Not configurable.

  - **`st2094-40`** EETF from SMPTE ST 2094-40 Annex B, which applies the Bezier curves from HDR10+ dynamic metadata based on Bezier curves to perform tone-mapping. The OOTF used is adjusted based on the ratio between the targeted and actual display peak luminances.

  - **`st2094-10`** EETF from SMPTE ST 2094-10 Annex B.2, which takes into account the input signal average luminance in addition to the maximum/minimum. The configurable contrast parameter influences the slope of the linear output segment, defaulting to `1.0` for no increase/decrease in contrast. Note that this does not currently include the subjective gain/offset/gamma controls defined in Annex B.3.

  - **`bt.2390`** EETF from the ITU-R Report BT.2390, a hermite spline roll-off with linear segment. The knee point offset is configurable. Note that this parameter defaults to `1.0`, rather than the value of `0.5` from the ITU-R spec.

  - **`bt.2446a`** EETF from ITU-R Report BT.2446, method A. Designed for well-mastered HDR sources. Can be used for both forward and inverse tone mapping. Not configurable.

  - **`spline`** Simple spline consisting of two polynomials, joined by a single pivot point. The parameter gives the pivot point (in PQ space), defaulting to `0.30`. Can be used for both forward and inverse tone mapping.

  - **`reinhard`** Simple non-linear, global tone mapping algorithm. The parameter specifies the local contrast coefficient at the display peak. Essentially, a parameter of `0.5` implies that the reference white will be about half as bright as when clipping. Defaults to `0.5`, which results in the simplest formulation of this function.

  - **`mobius`** Generalization of the reinhard tone mapping algorithm to support an additional linear slope near black. The tone mapping parameter indicates the trade-off between the linear section and the non-linear section. Essentially, for a given parameter \<x\>, every color value below \<x\> will be mapped linearly, while higher values get non-linearly tone-mapped. Values near `1.0` make this curve behave like `clip`, while values near `0.0` make this curve behave like `reinhard`. The default value is `0.3`, which provides a good balance between colorimetric accuracy and preserving out-of-gamut details.

  - **`hable`** Piece-wise, filmic tone-mapping algorithm developed by John Hable for use in Uncharted 2, inspired by a similar tone-mapping algorithm used by Kodak. Popularized by its use in video games with HDR rendering. Preserves both dark and bright details very well, but comes with the drawback of changing the average brightness quite significantly. This is sort of similar to `reinhard` with parameter `0.24`.

  - **`gamma`** Fits a gamma (power) function to transfer between the source and target color spaces, effectively resulting in a perceptual hard-knee joining two roughly linear sections. This preserves details at all scales fairly accurately, but can result in an image with a muted or dull appearance. The parameter is used as the cutoff point, defaulting to `0.5`.

  - **`linear`** Linearly stretches the input range to the output range, in PQ space. This will preserve all details accurately, but results in a significantly different average brightness. Can be used for inverse tone-mapping in addition to regular tone-mapping. The parameter can be used as an additional linear gain coefficient (defaulting to `1.0`).

- **`tonemapping_param`** For tunable tone mapping functions, this parameter can be used to fine-tune the curve behavior. Refer to the documentation of `tonemapping`. The default value of `0.0` is replaced by the curve's preferred default setting.

- **`inverse_tonemapping`** If enabled, this filter will also attempt stretching SDR signals to fill HDR output color volumes. Disabled by default.

- **`tonemapping_lut_size`** Size of the tone-mapping LUT, between `2` and `1024`. Defaults to `256`. Note that this figure is squared when combined with `peak_detect`.

- **`contrast_recovery`** Contrast recovery strength. If set to a value above `0.0`, the source image will be divided into high-frequency and low-frequency components, and a portion of the high-frequency image is added back onto the tone-mapped output. May cause excessive ringing artifacts for some HDR sources, but can improve the subjective sharpness and detail left over in the image after tone-mapping. Defaults to `0.30`.

- **`contrast_smoothness`** Contrast recovery lowpass kernel size. Defaults to `3.5`. Increasing or decreasing this will affect the visual appearance substantially. Has no effect when `contrast_recovery` is disabled.

### Dithering

By default, libplacebo will dither whenever necessary, which includes rendering to any integer format below 16-bit precision. It's recommended to always leave this on, since not doing so may result in visible banding in the output, even if the `debanding` filter is enabled. If maximum performance is needed, use `ordered_fixed` instead of disabling dithering.

- **`dithering`** Dithering method to use. Accepts the following values:

  - **`none`** Disables dithering completely. May result in visible banding.

  - **`blue`** Dither with pseudo-blue noise. This is the default.

  - **`ordered`** Tunable ordered dither pattern.

  - **`ordered_fixed`** Faster ordered dither with a fixed size of `6`. Texture-less.

  - **`white`** Dither with white noise. Texture-less.

- **`dither_lut_size`** Dither LUT size, as log base2 between `1` and `8`. Defaults to `6`, corresponding to a LUT size of `64x64`.

- **`dither_temporal`** Enables temporal dithering. Disabled by default.

### Custom shaders

libplacebo supports a number of custom shaders based on the mpv .hook GLSL syntax. A collection of such shaders can be found here: <https://github.com/mpv-player/mpv/wiki/User-Scripts#user-shaders>

A full description of the mpv shader format is beyond the scope of this section, but a summary can be found here: <https://mpv.io/manual/master/#options-glsl-shader>

| Term | Description |
|----|----|
| `custom_shader_path` | Specifies a path to a custom shader file to load at runtime. |
| `custom_shader_bin` | Specifies a complete custom shader as a raw string. |

### Debugging / performance

All of the options in this section default off. They may be of assistance when attempting to squeeze the maximum performance at the cost of quality.

- **`skip_aa`** Disable anti-aliasing when downscaling.

- **`disable_linear`** Disable linear light scaling.

- **`disable_builtin`** Disable built-in GPU sampling (forces LUT).

- **`disable_fbos`** Forcibly disable FBOs, resulting in loss of almost all functionality, but offering the maximum possible speed.

## Commands

This filter supports almost all of the above options as [commands](#commands).

## Examples

- Tone-map input to standard gamut BT.709 output:

  ``` text
  libplacebo=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv
  ```

- Rescale input to fit into standard 1080p, with high quality scaling:

  ``` text
  libplacebo=w=1920:h=1080:force_original_aspect_ratio=decrease:normalize_sar=true:upscaler=ewa_lanczos:downscaler=ewa_lanczos
  ```

- Interpolate low FPS / VFR input to smoothed constant 60 fps output:

  ``` text
  libplacebo=fps=60:frame_mixer=mitchell_clamp
  ```

- Convert input to standard sRGB JPEG:

  ``` text
  libplacebo=format=yuv420p:colorspace=bt470bg:color_primaries=bt709:color_trc=iec61966-2-1:range=pc
  ```

- Use higher quality debanding settings:

  ``` text
  libplacebo=deband=true:deband_iterations=3:deband_radius=8:deband_threshold=6
  ```

- Run this filter on the CPU, on systems with Mesa installed (and with the most expensive options disabled):

  ``` text
  ffmpeg ... -init_hw_device vulkan:llvmpipe ... -vf libplacebo=upscaler=none:downscaler=none:peak_detect=false
  ```

- Suppress CPU-based AV1/H.274 film grain application in the decoder, in favor of doing it with this filter. Note that this is only a gain if the frames are either already on the GPU, or if you're using libplacebo for other purposes, since otherwise the VRAM roundtrip will more than offset any expected speedup.

  ``` text
  ffmpeg -export_side_data +film_grain ... -vf libplacebo=apply_filmgrain=true
  ```

- Interop with VAAPI hwdec to avoid round-tripping through RAM:

  ``` text
  ffmpeg -init_hw_device vulkan -hwaccel vaapi -hwaccel_output_format vaapi ... -vf libplacebo
  ```
