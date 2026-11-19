# agate

A gate is mainly used to reduce lower parts of a signal. This kind of signal processing reduces disturbing noise between useful signals.

Gating is done by detecting the volume below a chosen level \<threshold\> and dividing it by the factor set with \<ratio\>. The bottom of the noise floor is set via \<range\>. Because an exact manipulation of the signal would cause distortion of the waveform the reduction can be levelled over time. This is done by setting \<attack\> and \<release\>.

\<attack\> determines how long the signal has to fall below the threshold before any reduction will occur and \<release\> sets the time the signal has to rise above the threshold to reduce the reduction again. Shorter signals than the chosen attack time will be left untouched.

- **`level_in`** Set input level before filtering. Default is 1. Allowed range is from 0.015625 to 64.

- **`mode`** Set the mode of operation. Can be `upward` or `downward`. Default is `downward`. If set to `upward` mode, higher parts of signal will be amplified, expanding dynamic range in upward direction. Otherwise, in case of `downward` lower parts of signal will be reduced.

- **`range`** Set the level of gain reduction when the signal is below the threshold. Default is 0.06125. Allowed range is from 0 to 1. Setting this to 0 disables reduction and then filter behaves like expander.

- **`threshold`** If a signal rises above this level the gain reduction is released. Default is 0.125. Allowed range is from 0 to 1.

- **`ratio`** Set a ratio by which the signal is reduced. Default is 2. Allowed range is from 1 to 9000.

- **`attack`** Amount of milliseconds the signal has to rise above the threshold before gain reduction stops. Default is 20 milliseconds. Allowed range is from 0.01 to 9000.

- **`release`** Amount of milliseconds the signal has to fall below the threshold before the reduction is increased again. Default is 250 milliseconds. Allowed range is from 0.01 to 9000.

- **`makeup`** Set amount of amplification of signal after processing. Default is 1. Allowed range is from 1 to 64.

- **`knee`** Curve the sharp knee around the threshold to enter gain reduction more softly. Default is 2.828427125. Allowed range is from 1 to 8.

- **`detection`** Choose if exact signal should be taken for detection or an RMS like one. Default is `rms`. Can be `peak` or `rms`.

- **`link`** Choose if the average level between all channels or the louder channel affects the reduction. Default is `average`. Can be `average` or `maximum`.

## Commands

This filter supports the all above options as [commands](#commands).
