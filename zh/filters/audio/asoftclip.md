# asoftclip

Apply audio soft clipping.

Soft clipping is a type of distortion effect where the amplitude of a signal is saturated along a smooth curve, rather than the abrupt shape of hard-clipping.

This filter accepts the following options:

- **`type`** Set type of soft-clipping.

  It accepts the following values:

  - **`hard`**

  - **`tanh`**

  - **`atan`**

  - **`cubic`**

  - **`exp`**

  - **`alg`**

  - **`quintic`**

  - **`sin`**

  - **`erf`**

- **`threshold`** Set threshold from where to start clipping. Default value is 0dB or 1.

- **`output`** Set gain applied to output. Default value is 0dB or 1.

- **`param`** Set additional parameter which controls sigmoid function.

- **`oversample`** Set oversampling factor.

## Commands

This filter supports the all above options as [commands](#commands).
