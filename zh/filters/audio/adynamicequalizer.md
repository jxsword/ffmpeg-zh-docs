# adynamicequalizer

Apply dynamic equalization to input audio stream.

A description of the accepted options follows.

- **`threshold`** Set the detection threshold used to trigger equalization. Threshold detection is using detection filter. Default value is 0. Allowed range is from 0 to 100.

- **`dfrequency`** Set the detection frequency in Hz used for detection filter used to trigger equalization. Default value is 1000 Hz. Allowed range is between 2 and 1000000 Hz.

- **`dqfactor`** Set the detection resonance factor for detection filter used to trigger equalization. Default value is 1. Allowed range is from 0.001 to 1000.

- **`tfrequency`** Set the target frequency of equalization filter. Default value is 1000 Hz. Allowed range is between 2 and 1000000 Hz.

- **`tqfactor`** Set the target resonance factor for target equalization filter. Default value is 1. Allowed range is from 0.001 to 1000.

- **`attack`** Set the amount of milliseconds the signal from detection has to rise above the detection threshold before equalization starts. Default is 20. Allowed range is between 1 and 2000.

- **`release`** Set the amount of milliseconds the signal from detection has to fall below the detection threshold before equalization ends. Default is 200. Allowed range is between 1 and 2000.

- **`ratio`** Set the ratio by which the equalization gain is raised. Default is 1. Allowed range is between 0 and 30.

- **`makeup`** Set the makeup offset by which the equalization gain is raised. Default is 0. Allowed range is between 0 and 100.

- **`range`** Set the max allowed cut/boost amount. Default is 50. Allowed range is from 1 to 200.

- **`mode`** Set the mode of filter operation, can be one of the following:

  | Term           | Description                                  |
  |----------------|----------------------------------------------|
  | `listen`     | Output only isolated detection signal.       |
  | `cutbelow`   | Cut frequencies below detection threshold.   |
  | `cutabove`   | Cut frequencies above detection threshold.   |
  | `boostbelow` | Boost frequencies below detection threshold. |
  | `boostabove` | Boost frequencies above detection threshold. |

  Default mode is `cutbelow`.

- **`dftype`** Set the type of detection filter, can be one of the following:

  - **`bandpass`**

  - **`lowpass`**

  - **`highpass`**

  - **`peak`**

  Default type is `bandpass`.

- **`tftype`** Set the type of target filter, can be one of the following:

  - **`bell`**

  - **`lowshelf`**

  - **`highshelf`**

  Default type is `bell`.

- **`auto`** Automatically gather threshold from detection filter. By default is `disabled`. This option is useful to detect threshold in certain time frame of input audio stream, in such case option value is changed at runtime.

  Available values are:

  | Term | Description |
  |----|----|
  | `disabled` | Disable using automatically gathered threshold value. |
  | `off` | Stop picking threshold value. |
  | `on` | Start picking threshold value. |
  | `adaptive` | Adaptively pick threshold value, by calculating sliding window entropy. |

- **`precision`** Set which precision to use when processing samples.

  | Term     | Description                                                  |
  |----------|--------------------------------------------------------------|
  | `auto`   | Auto pick internal sample format depending on other filters. |
  | `float`  | Always use single-floating point precision sample format.    |
  | `double` | Always use double-floating point precision sample format.    |

## Commands

This filter supports the all above options as [commands](#commands).
