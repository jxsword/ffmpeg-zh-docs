# ocio

OpenColorIO library filter

This filter allows you to do color management using the OpenColorIO library. See https://opencolorio.org/ for more details. To Enable compilation of this filter, you need to configure FFmpeg with `--enable-libopencolorio`.

It accepts the following options:

- **`config`** By default the filter will use the OCIO config defined by the OCIO environment variable, but this parameter allows you to explicitly specify its location. If you are getting started, you can use config=ocio://studio-config-v1.0.0_aces-v1.3_ocio-v2.1 which specifies one of the built in defaults.

- **`input`** Set the input colorspace.

- **`output`** Set the output colorspace.

- **`display`** Set the display colorspace, used in combination with view.

- **`view`** Set the view colorspace, used in combination with display.

- **`inverse`** When used in combination with display and view, this inverts the transform, so going from a display/view to the "input colorspace".

- **`filetransform`** Allows you to specify an external file-transform to use instead of the OCIO config file. This is useful for applying a single transform without needing a full OCIO config file.

- **`format`** Allow you to specify the output pix_fmt of the OCIO filter. This \*has\* to be a RGB colorspace, so you really are limited to rgb24, rgba, rgb48, rgba48, gbrp10, gbrp12, gbrpf32le, gbrapf32le, for most encoding we would recommend rgb48

- **`context_params`** Allow you to specify additional context parameters for the OCIO filter. This is a list of key=value pairs, separated by colons.

## Examples

Map from ACEScg to ACEScct, this assumes the OCIO file is defined with the OCIO environment variable.

``` text
input=ACEScg:output=ACEScct:format=rgb48
```

Map from ACEScg to a sRGB display using the "ACES 1.0 - SDR Video" view transform, this assumes the OCIO file is defined with the OCIO environment variable. Note you will need to wrap the argument in quotes to ensure that the spaces are interpreted correctly.

``` text
input=ACEScg:display=sRGB - Display:view=ACES 1.0 - SDR Video:format=rgb48
```

As above but using the OCIO file studio-config-v1.0.0_aces-v1.3_ocio-v2.1_ns.ocio rather than the OCIO environment variable.

``` text
config=studio-config-v1.0.0_aces-v1.3_ocio-v2.1_ns.ocio:input=ACEScg:display=sRGB - Display:view=ACES 1.0 - SDR Video:format=rgb48
```

If you are converting to YCrCb you still will want to set the color matrix for the conversion. This is a good example of combining the two.

``` text
ffmpeg -y -i SOURCEFRAMES.%05d.exr -c:v libx265 -vf "ocio=input=ACEScg:output=ACEScct:format=rgb48,scale=in_color_matrix=bt709:out_color_matrix=bt709,format=yuv444p10"  OUTPUTFILE.mov
```
