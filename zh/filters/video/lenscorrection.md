# lenscorrection

Correct radial lens distortion

This filter can be used to correct for radial distortion as can result from the use of wide angle lenses, and thereby re-rectify the image. To find the right parameters one can use tools available for example as part of opencv or simply trial-and-error. To use opencv use the calibration sample (under samples/cpp) from the opencv sources and extract the k1 and k2 coefficients from the resulting matrix.

Note that effectively the same filter is available in the open-source tools Krita and Digikam from the KDE project.

In contrast to the [vignette](vignette.md#vignette) filter, which can also be used to compensate lens errors, this filter corrects the distortion of the image, whereas [vignette](vignette.md#vignette) corrects the brightness distribution, so you may want to use both filters together in certain cases, though you will have to take care of ordering, i.e. whether vignetting should be applied before or after lens correction.

## Options

The filter accepts the following options:

- **`cx`** Relative x-coordinate of the focal point of the image, and thereby the center of the distortion. This value has a range \[0,1\] and is expressed as fractions of the image width. Default is 0.5.

- **`cy`** Relative y-coordinate of the focal point of the image, and thereby the center of the distortion. This value has a range \[0,1\] and is expressed as fractions of the image height. Default is 0.5.

- **`k1`** Coefficient of the quadratic correction term. This value has a range \[-1,1\]. 0 means no correction. Default is 0.

- **`k2`** Coefficient of the double quadratic correction term. This value has a range \[-1,1\]. 0 means no correction. Default is 0.

- **`i`** Set interpolation type. Can be `nearest` or `bilinear`. Default is `nearest`.

- **`fc`** Specify the color of the unmapped pixels. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default color is `black@0`.

The formula that generates the correction is:

\<r_src\> = \<r_tgt\> \* (1 + \<k1\> \* (\<r_tgt\> / \<r_0\>)^2 + \<k2\> \* (\<r_tgt\> / \<r_0\>)^4)

where \<r_0\> is halve of the image diagonal and \<r_src\> and \<r_tgt\> are the distances from the focal point in the source and target images, respectively.

## Commands

This filter supports the all above options as [commands](#commands).
