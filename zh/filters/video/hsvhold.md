# hsvhold

Turns a certain HSV range into gray values.

This filter measures color difference between set HSV color in options and ones measured in video stream. Depending on options, output colors can be changed to be gray or not.

The filter accepts the following options:

- **`hue`** Set the hue value which will be used in color difference calculation. Allowed range is from -360 to 360. Default value is 0.

- **`sat`** Set the saturation value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.

- **`val`** Set the value which will be used in color difference calculation. Allowed range is from -1 to 1. Default value is 0.

- **`similarity`** Set similarity percentage with the key color. Allowed range is from 0 to 1. Default value is 0.01.

  0.00001 matches only the exact key color, while 1.0 matches everything.

- **`blend`** Blend percentage. Allowed range is from 0 to 1. Default value is 0.

  0.0 makes pixels either fully gray, or not gray at all.

  Higher values result in more gray pixels, with a higher gray pixel the more similar the pixels color is to the key color.
