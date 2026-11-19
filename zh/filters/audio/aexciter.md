# aexciter

An exciter is used to produce high sound that is not present in the original signal. This is done by creating harmonic distortions of the signal which are restricted in range and added to the original signal. An Exciter raises the upper end of an audio signal without simply raising the higher frequencies like an equalizer would do to create a more "crisp" or "brilliant" sound.

The filter accepts the following options:

- **`level_in`** Set input level prior processing of signal. Allowed range is from 0 to 64. Default value is 1.

- **`level_out`** Set output level after processing of signal. Allowed range is from 0 to 64. Default value is 1.

- **`amount`** Set the amount of harmonics added to original signal. Allowed range is from 0 to 64. Default value is 1.

- **`drive`** Set the amount of newly created harmonics. Allowed range is from 0.1 to 10. Default value is 8.5.

- **`blend`** Set the octave of newly created harmonics. Allowed range is from -10 to 10. Default value is 0.

- **`freq`** Set the lower frequency limit of producing harmonics in Hz. Allowed range is from 2000 to 12000 Hz. Default is 7500 Hz.

- **`ceil`** Set the upper frequency limit of producing harmonics. Allowed range is from 9999 to 20000 Hz. If value is lower than 10000 Hz no limit is applied.

- **`listen`** Mute the original signal and output only added harmonics. By default is disabled.

## Commands

This filter supports the all above options as [commands](#commands).
