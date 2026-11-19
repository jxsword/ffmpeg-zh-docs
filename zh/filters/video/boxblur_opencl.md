# boxblur_opencl

Apply a boxblur algorithm to the input video.

It accepts the following parameters:

- **`luma_radius, lr`**

- **`luma_power, lp`**

- **`chroma_radius, cr`**

- **`chroma_power, cp`**

- **`alpha_radius, ar`**

- **`alpha_power, ap`**

A description of the accepted options follows.

- **`luma_radius, lr`**

- **`chroma_radius, cr`**

- **`alpha_radius, ar`** Set an expression for the box radius in pixels used for blurring the corresponding input plane.

  The radius value must be a non-negative number, and must not be greater than the value of the expression `min(w,h)/2` for the luma and alpha planes, and of `min(cw,ch)/2` for the chroma planes.

  Default value for `luma_radius` is "2". If not specified, `chroma_radius` and `alpha_radius` default to the corresponding value set for `luma_radius`.

  The expressions can contain the following constants:

  - **`w`**

  - **`h`** The input width and height in pixels.

  - **`cw`**

  - **`ch`** The input chroma image width and height in pixels.

  - **`hsub`**

  - **`vsub`** The horizontal and vertical chroma subsample values. For example, for the pixel format "yuv422p", \<hsub\> is 2 and \<vsub\> is 1.

- **`luma_power, lp`**

- **`chroma_power, cp`**

- **`alpha_power, ap`** Specify how many times the boxblur filter is applied to the corresponding plane.

  Default value for `luma_power` is 2. If not specified, `chroma_power` and `alpha_power` default to the corresponding value set for `luma_power`.

  A value of 0 will disable the effect.

## Examples

Apply boxblur filter, setting each pixel of the output to the average value of box-radiuses \<luma_radius\>, \<chroma_radius\>, \<alpha_radius\> for each plane respectively. The filter will apply \<luma_power\>, \<chroma_power\>, \<alpha_power\> times onto the corresponding plane. For pixels on the edges of the image, the radius does not extend beyond the image boundaries, and so out-of-range coordinates are not used in the calculations.

- Apply a boxblur filter with the luma, chroma, and alpha radius set to 2 and luma, chroma, and alpha power set to 3. The filter will run 3 times with box-radius set to 2 for every plane of the image.

  ``` text
  -i INPUT -vf "hwupload, boxblur_opencl=luma_radius=2:luma_power=3, hwdownload" OUTPUT
  -i INPUT -vf "hwupload, boxblur_opencl=2:3, hwdownload" OUTPUT
  ```

- Apply a boxblur filter with luma radius set to 2, luma_power to 1, chroma_radius to 4, chroma_power to 5, alpha_radius to 3 and alpha_power to 7.

  For the luma plane, a 2x2 box radius will be run once.

  For the chroma plane, a 4x4 box radius will be run 5 times.

  For the alpha plane, a 3x3 box radius will be run 7 times.

  ``` text
  -i INPUT -vf "hwupload, boxblur_opencl=2:1:4:5:3:7, hwdownload" OUTPUT
  ```
