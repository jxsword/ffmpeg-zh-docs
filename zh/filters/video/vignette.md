# vignette

Make or reverse a natural vignetting effect.

The filter accepts the following options:

- **`angle, a`** Set lens angle expression as a number of radians.

  The value is clipped in the `[0,PI/2]` range.

  Default value: `"PI/5"`

- **`x0`**

- **`y0`** Set center coordinates expressions. Respectively `"w/2"` and `"h/2"` by default.

- **`mode`** Set forward/backward mode.

  Available modes are:

  - **`forward`** The larger the distance from the central point, the darker the image becomes.

  - **`backward`** The larger the distance from the central point, the brighter the image becomes. This can be used to reverse a vignette effect, though there is no automatic detection to extract the lens `angle` and other settings (yet). It can also be used to create a burning effect.

  Default value is `forward`.

- **`eval`** Set evaluation mode for the expressions (`angle`, `x0`, `y0`).

  It accepts the following values:

  - **`init`** Evaluate expressions only once during the filter initialization.

  - **`frame`** Evaluate expressions for each incoming frame. This is way slower than the `init` mode since it requires all the scalers to be re-computed, but it allows advanced dynamic expressions.

  Default value is `init`.

- **`dither`** Set dithering to reduce the circular banding effects. Default is `1` (enabled).

- **`aspect`** Set vignette aspect. This setting allows one to adjust the shape of the vignette. Setting this value to the SAR of the input will make a rectangular vignetting following the dimensions of the video.

  Default is `1/1`.

## Expressions

The `alpha`, `x0` and `y0` expressions can contain the following parameters.

- **`w`**

- **`h`** input width and height

- **`n`** the number of input frame, starting from 0

- **`pts`** the PTS (Presentation TimeStamp) time of the filtered video frame, expressed in \<TB\> units, NAN if undefined

- **`r`** frame rate of the input video, NAN if the input frame rate is unknown

- **`t`** the PTS (Presentation TimeStamp) of the filtered video frame, expressed in seconds, NAN if undefined

- **`tb`** time base of the input video

## Examples

- Apply simple strong vignetting effect:

  ``` text
  vignette=PI/4
  ```

- Make a flickering vignetting:

  ``` text
  vignette='PI/4+random(1)*PI/50':eval=frame
  ```
