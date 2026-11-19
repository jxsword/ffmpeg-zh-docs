# hilbert

Generate odd-tap Hilbert transform FIR coefficients.

The resulting stream can be used with [afir](afir.md#afir) filter for phase-shifting the signal by 90 degrees.

This is used in many matrix coding schemes and for analytic signal generation. The process is often written as a multiplication by i (or j), the imaginary unit.

The filter accepts the following options:

| Term | Description |
|----|----|
| `sample_rate, s` | Set sample rate, default is 44100. |
| `taps, t` | Set length of FIR filter, default is 22051. |
| `nb_samples, n` | Set number of samples per each frame. |
| `win_func, w` | Set window function to be used when generating FIR coefficients. |
