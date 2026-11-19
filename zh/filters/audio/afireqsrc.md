# afireqsrc

Generate a FIR equalizer coefficients.

The resulting stream can be used with [afir](afir.md#afir) filter for filtering the audio signal.

The filter accepts the following options:

- **`preset, p`** Set equalizer preset. Default preset is `flat`.

  Available presets are:

  - **`custom`**

  - **`flat`**

  - **`acoustic`**

  - **`bass`**

  - **`beats`**

  - **`classic`**

  - **`clear`**

  - **`deep bass`**

  - **`dubstep`**

  - **`electronic`**

  - **`hard-style`**

  - **`hip-hop`**

  - **`jazz`**

  - **`metal`**

  - **`movie`**

  - **`pop`**

  - **`r&b`**

  - **`rock`**

  - **`vocal booster`**

- **`gains, g`** Set custom gains for each band. Only used if the preset option is set to `custom`. Gains are separated by white spaces and each gain is set in dBFS. Default is `0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0`.

- **`bands, b`** Set the custom bands from where custom equalizer gains are set. This must be in strictly increasing order. Only used if the preset option is set to `custom`. Bands are separated by white spaces and each band represent frequency in Hz. Default is `25 40 63 100 160 250 400 630 1000 1600 2500 4000 6300 10000 16000 24000`.

- **`taps, t`** Set number of filter coefficients in output audio stream. Default value is `4096`.

- **`sample_rate, r`** Set sample rate of output audio stream, default is `44100`.

- **`nb_samples, n`** Set number of samples per each frame in output audio stream. Default is `1024`.

- **`interp, i`** Set interpolation method for FIR equalizer coefficients. Can be `linear` or `cubic`.

- **`phase, h`** Set phase type of FIR filter. Can be `linear` or `min`: minimum-phase. Default is minimum-phase filter.
