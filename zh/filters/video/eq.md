# eq

Set brightness, contrast, saturation and approximate gamma adjustment.

The filter accepts the following options:

- **`contrast`** Set the contrast expression. The value must be a float value in range `-1000.0` to `1000.0`. The default value is "1".

- **`brightness`** Set the brightness expression. The value must be a float value in range `-1.0` to `1.0`. The default value is "0".

- **`saturation`** Set the saturation expression. The value must be a float in range `0.0` to `3.0`. The default value is "1".

- **`gamma`** Set the gamma expression. The value must be a float in range `0.1` to `10.0`. The default value is "1".

- **`gamma_r`** Set the gamma expression for red. The value must be a float in range `0.1` to `10.0`. The default value is "1".

- **`gamma_g`** Set the gamma expression for green. The value must be a float in range `0.1` to `10.0`. The default value is "1".

- **`gamma_b`** Set the gamma expression for blue. The value must be a float in range `0.1` to `10.0`. The default value is "1".

- **`gamma_weight`** Set the gamma weight expression. It can be used to reduce the effect of a high gamma value on bright image areas, e.g. keep them from getting overamplified and just plain white. The value must be a float in range `0.0` to `1.0`. A value of `0.0` turns the gamma correction all the way down while `1.0` leaves it at its full strength. Default is "1".

- **`eval`** Set when the expressions for brightness, contrast, saturation and gamma expressions are evaluated.

  It accepts the following values:

  - **`init`** only evaluate expressions once during the filter initialization or when a command is processed

  - **`frame`** evaluate expressions for each incoming frame

  Default value is `init`.

The expressions accept the following parameters:

- **`n`** frame count of the input frame starting from 0

- **`pos`** byte position of the corresponding packet in the input file, NAN if unspecified; deprecated, do not use

- **`r`** frame rate of the input video, NAN if the input frame rate is unknown

- **`t`** timestamp expressed in seconds, NAN if the input timestamp is unknown

## Commands

The filter supports the following commands:

- **`contrast`** Set the contrast expression.

- **`brightness`** Set the brightness expression.

- **`saturation`** Set the saturation expression.

- **`gamma`** Set the gamma expression.

- **`gamma_r`** Set the gamma_r expression.

- **`gamma_g`** Set gamma_g expression.

- **`gamma_b`** Set gamma_b expression.

- **`gamma_weight`** Set gamma_weight expression.

  The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
