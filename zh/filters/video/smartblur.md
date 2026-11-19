# smartblur

Blur the input video without impacting the outlines.

It accepts the following options:

- **`luma_radius, lr`** Set the luma radius. The option value must be a float number in the range \[0.1,5.0\] that specifies the variance of the gaussian filter used to blur the image (slower if larger). Default value is 1.0.

- **`luma_strength, ls`** Set the luma strength. The option value must be a float number in the range \[-1.0,1.0\] that configures the blurring. A value included in \[0.0,1.0\] will blur the image whereas a value included in \[-1.0,0.0\] will sharpen the image. Default value is 1.0.

- **`luma_threshold, lt`** Set the luma threshold used as a coefficient to determine whether a pixel should be blurred or not. The option value must be an integer in the range \[-30,30\]. A value of 0 will filter all the image, a value included in \[0,30\] will filter flat areas and a value included in \[-30,0\] will filter edges. Default value is 0.

- **`chroma_radius, cr`** Set the chroma radius. The option value must be a float number in the range \[0.1,5.0\] that specifies the variance of the gaussian filter used to blur the image (slower if larger). Default value is `luma_radius`.

- **`chroma_strength, cs`** Set the chroma strength. The option value must be a float number in the range \[-1.0,1.0\] that configures the blurring. A value included in \[0.0,1.0\] will blur the image whereas a value included in \[-1.0,0.0\] will sharpen the image. Default value is `luma_strength`.

- **`chroma_threshold, ct`** Set the chroma threshold used as a coefficient to determine whether a pixel should be blurred or not. The option value must be an integer in the range \[-30,30\]. A value of 0 will filter all the image, a value included in \[0,30\] will filter flat areas and a value included in \[-30,0\] will filter edges. Default value is `luma_threshold`.

- **`alpha_radius, ar`** Set the alpha radius. The option value must be a float number in the range \[0.1,5.0\] that specifies the variance of the gaussian filter used to blur the image (slower if larger). Default value is `luma_radius`.

- **`alpha_strength, as`** Set the alpha strength. The option value must be a float number in the range \[-1.0,1.0\] that configures the blurring. A value included in \[0.0,1.0\] will blur the image whereas a value included in \[-1.0,0.0\] will sharpen the image. Default value is `luma_strength`.

- **`alpha_threshold, at`** Set the alpha threshold used as a coefficient to determine whether a pixel should be blurred or not. The option value must be an integer in the range \[-30,30\]. A value of 0 will filter all the image, a value included in \[0,30\] will filter flat areas and a value included in \[-30,0\] will filter edges. Default value is `luma_threshold`.

If a chroma or alpha option is not explicitly set, the corresponding luma value is set.
