# alimiter

The limiter prevents an input signal from rising over a desired threshold. This limiter uses lookahead technology to prevent your signal from distorting. It means that there is a small delay after the signal is processed. Keep in mind that the delay it produces is the attack time you set.

The filter accepts the following options:

- **`level_in`** Set input gain. Default is 1.

- **`level_out`** Set output gain. Default is 1.

- **`limit`** Don't let signals above this level pass the limiter. Default is 1.

- **`attack`** The limiter will reach its attenuation level in this amount of time in milliseconds. Default is 5 milliseconds.

- **`release`** Come back from limiting to attenuation 1.0 in this amount of milliseconds. Default is 50 milliseconds.

- **`asc`** When gain reduction is always needed ASC takes care of releasing to an average reduction level rather than reaching a reduction of 0 in the release time.

- **`asc_level`** Select how much the release time is affected by ASC, 0 means nearly no changes in release time while 1 produces higher release times.

- **`level`** Auto level output signal. Default is enabled. This normalizes audio back to 0dB if enabled.

- **`latency`** Compensate the delay introduced by using the lookahead buffer set with attack parameter. Also flush the valid audio data in the lookahead buffer when the stream hits EOF.

Depending on picked setting it is recommended to upsample input 2x or 4x times with [aresample](aresample.md#aresample) before applying this filter.
