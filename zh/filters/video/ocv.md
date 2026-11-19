# ocv

Apply a video transform using libopencv.

To enable this filter, install the libopencv library and headers and configure FFmpeg with `--enable-libopencv`.

It accepts the following parameters:

- **`filter_name`** The name of the libopencv filter to apply.

- **`filter_params`** The parameters to pass to the libopencv filter. If not specified, the default values are assumed.

Refer to the official libopencv documentation for more precise information: <http://docs.opencv.org/master/modules/imgproc/doc/filtering.html>

Several libopencv filters are supported; see the following subsections.

## dilate

Dilate an image by using a specific structuring element. It corresponds to the libopencv function `cvDilate`.

It accepts the parameters: \<struct_el\>\|\<nb_iterations\>.

\<struct_el\> represents a structuring element, and has the syntax: \<cols\>x\<rows\>+\<anchor_x\>x\<anchor_y\>/\<shape\>

\<cols\> and \<rows\> represent the number of columns and rows of the structuring element, \<anchor_x\> and \<anchor_y\> the anchor point, and \<shape\> the shape for the structuring element. \<shape\> must be "rect", "cross", "ellipse", or "custom".

If the value for \<shape\> is "custom", it must be followed by a string of the form "=\<filename\>". The file with name \<filename\> is assumed to represent a binary image, with each printable character corresponding to a bright pixel. When a custom \<shape\> is used, \<cols\> and \<rows\> are ignored, the number or columns and rows of the read file are assumed instead.

The default value for \<struct_el\> is "3x3+0x0/rect".

\<nb_iterations\> specifies the number of times the transform is applied to the image, and defaults to 1.

Some examples:

``` text
# Use the default values
ocv=dilate

# Dilate using a structuring element with a 5x5 cross, iterating two times
ocv=filter_name=dilate:filter_params=5x5+2x2/cross|2

# Read the shape from the file diamond.shape, iterating two times.
# The file diamond.shape may contain a pattern of characters like this
#   *
#  ***
# *****
#  ***
#   *
# The specified columns and rows are ignored
# but the anchor point coordinates are not
ocv=dilate:0x0+2x2/custom=diamond.shape|2
```

## erode

Erode an image by using a specific structuring element. It corresponds to the libopencv function `cvErode`.

It accepts the parameters: \<struct_el\>:\<nb_iterations\>, with the same syntax and semantics as the [dilate](#dilate) filter.

## smooth

Smooth the input video.

The filter takes the following parameters: \<type\>\|\<param1\>\|\<param2\>\|\<param3\>\|\<param4\>.

\<type\> is the type of smooth filter to apply, and must be one of the following values: "blur", "blur_no_scale", "median", "gaussian", or "bilateral". The default value is "gaussian".

The meaning of \<param1\>, \<param2\>, \<param3\>, and \<param4\> depends on the smooth type. \<param1\> and \<param2\> accept integer positive values or 0. \<param3\> and \<param4\> accept floating point values.

The default value for \<param1\> is 3. The default value for the other parameters is 0.

These parameters correspond to the parameters assigned to the libopencv function `cvSmooth`.
