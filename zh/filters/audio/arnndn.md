# arnndn

Reduce noise from speech using Recurrent Neural Networks.

This filter accepts the following options:

- **`model, m`** Set train model file to load. This option is always required.

- **`mix`** Set how much to mix filtered samples into final output. Allowed range is from -1 to 1. Default value is 1. Negative values are special, they set how much to keep filtered noise in the final filter output. Set this option to -1 to hear actual noise removed from input signal.

## Commands

This filter supports the all above options as [commands](#commands).
