# tonemap

Tone map colors from different dynamic ranges.

This filter expects data in single precision floating point, as it needs to operate on (and can output) out-of-range values. Another filter, such as [zscale](zscale.md#zscale), is needed to convert the resulting frame to a usable format.

The tonemapping algorithms implemented only work on linear light, so input data should be linearized beforehand (and possibly correctly tagged).

``` text
ffmpeg -i INPUT -vf zscale=transfer=linear,tonemap=clip,zscale=transfer=bt709,format=yuv420p OUTPUT
```

## Options

The filter accepts the following options.

- **`tonemap`** Set the tone map algorithm to use.

  Possible values are:

  - **\<none\>** Do not apply any tone map, only desaturate overbright pixels.

  - **\<clip\>** Hard-clip any out-of-range values. Use it for perfect color accuracy for in-range values, while distorting out-of-range values.

  - **\<linear\>** Stretch the entire reference gamut to a linear multiple of the display.

  - **\<gamma\>** Fit a logarithmic transfer between the tone curves.

  - **\<reinhard\>** Preserve overall image brightness with a simple curve, using nonlinear contrast, which results in flattening details and degrading color accuracy.

  - **\<hable\>** Preserve both dark and bright details better than \<reinhard\>, at the cost of slightly darkening everything. Use it when detail preservation is more important than color and brightness accuracy.

  - **\<mobius\>** Smoothly map out-of-range values, while retaining contrast and colors for in-range material as much as possible. Use it when color accuracy is more important than detail preservation.

  Default is none.

- **`param`** Tune the tone mapping algorithm.

  This affects the following algorithms:

  - **\<none\>** Ignored.

  - **\<linear\>** Specifies the scale factor to use while stretching. Default to 1.0.

  - **\<gamma\>** Specifies the exponent of the function. Default to 1.8.

  - **\<clip\>** Specify an extra linear coefficient to multiply into the signal before clipping. Default to 1.0.

  - **\<reinhard\>** Specify the local contrast coefficient at the display peak. Default to 0.5, which means that in-gamut values will be about half as bright as when clipping.

  - **\<hable\>** Ignored.

  - **\<mobius\>** Specify the transition point from linear to mobius transform. Every value below this point is guaranteed to be mapped 1:1. The higher the value, the more accurate the result will be, at the cost of losing bright details. Default to 0.3, which due to the steep initial slope still preserves in-range colors fairly accurately.

- **`desat`** Apply desaturation for highlights that exceed this level of brightness. The higher the parameter, the more color information will be preserved. This setting helps prevent unnaturally blown-out colors for super-highlights, by (smoothly) turning into white instead. This makes images feel more natural, at the cost of reducing information about out-of-range colors.

  The default of 2.0 is somewhat conservative and will mostly just apply to skies or directly sunlit surfaces. A setting of 0.0 disables this option.

  This option works only if the input frame has a supported color tag.

- **`peak`** Override signal/nominal/reference peak with this value. Useful when the embedded peak information in display metadata is not reliable or when tone mapping from a lower range to a higher range.
