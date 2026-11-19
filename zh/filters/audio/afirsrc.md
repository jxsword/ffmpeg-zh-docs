# afirsrc

Generate a FIR coefficients using frequency sampling method.

The resulting stream can be used with [afir](afir.md#afir) filter for filtering the audio signal.

The filter accepts the following options:

- **`taps, t`** Set number of filter coefficients in output audio stream. Default value is 1025.

- **`frequency, f`** Set frequency points from where magnitude and phase are set. This must be in non decreasing order, and first element must be 0, while last element must be 1. Elements are separated by white spaces.

- **`magnitude, m`** Set magnitude value for every frequency point set by `frequency`. Number of values must be same as number of frequency points. Values are separated by white spaces.

- **`phase, p`** Set phase value for every frequency point set by `frequency`. Number of values must be same as number of frequency points. Values are separated by white spaces.

- **`sample_rate, r`** Set sample rate, default is 44100.

- **`nb_samples, n`** Set number of samples per each frame. Default is 1024.

- **`win_func, w`** Set window function. Default is blackman.
