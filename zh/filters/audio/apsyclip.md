# apsyclip

Apply Psychoacoustic clipper to input audio stream.

The filter accepts the following options:

- **`level_in`** Set input gain. By default it is 1. Range is \[0.015625 - 64\].

- **`level_out`** Set output gain. By default it is 1. Range is \[0.015625 - 64\].

- **`clip`** Set the clipping start value. Default value is 0dBFS or 1.

- **`diff`** Output only difference samples, useful to hear introduced distortions. By default is disabled.

- **`adaptive`** Set strength of adaptive distortion applied. Default value is 0.5. Allowed range is from 0 to 1.

- **`iterations`** Set number of iterations of psychoacoustic clipper. Allowed range is from 1 to 20. Default value is 10.

- **`level`** Auto level output signal. Default is disabled. This normalizes audio back to 0dBFS if enabled.

## Commands

This filter supports the all above options as [commands](#commands).
