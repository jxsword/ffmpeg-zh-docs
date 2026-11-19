# setdar, setsar

The `setdar` filter sets the Display Aspect Ratio for the filter output video.

This is done by changing the specified Sample (aka Pixel) Aspect Ratio, according to the following equation:

``` text
DAR = HORIZONTAL_RESOLUTION / VERTICAL_RESOLUTION * SAR
```

Keep in mind that the `setdar` filter does not modify the pixel dimensions of the video frame. Also, the display aspect ratio set by this filter may be changed by later filters in the filterchain, e.g. in case of scaling or if another "setdar" or a "setsar" filter is applied.

The `setsar` filter sets the Sample (aka Pixel) Aspect Ratio for the filter output video.

Note that as a consequence of the application of this filter, the output display aspect ratio will change according to the equation above.

Keep in mind that the sample aspect ratio set by the `setsar` filter may be changed by later filters in the filterchain, e.g. if another "setsar" or a "setdar" filter is applied.

It accepts the following parameters:

- **`r, ratio, dar (setdar only), sar (setsar only)`** Set the aspect ratio used by the filter.

  The parameter can be a floating point number string, or an expression. If the parameter is not specified, the value "0" is assumed, meaning that the same input value is used.

- **`max`** Set the maximum integer value to use for expressing numerator and denominator when reducing the expressed aspect ratio to a rational. Default value is `100`.

The parameter \<sar\> is an expression containing the following constants:

- **`w, h`** The input width and height.

- **`a`** Same as \<w\> / \<h\>.

- **`sar`** The input sample aspect ratio.

- **`dar`** The input display aspect ratio. It is the same as (\<w\> / \<h\>) \* \<sar\>.

- **`hsub, vsub`** Horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

## Examples

- To change the display aspect ratio to 16:9, specify one of the following:

  ``` text
  setdar=dar=1.77777
  setdar=dar=16/9
  ```

- To change the sample aspect ratio to 10:11, specify:

  ``` text
  setsar=sar=10/11
  ```

- To set a display aspect ratio of 16:9, and specify a maximum integer value of 1000 in the aspect ratio reduction, use the command:

  ``` text
  setdar=ratio=16/9:max=1000
  ```
