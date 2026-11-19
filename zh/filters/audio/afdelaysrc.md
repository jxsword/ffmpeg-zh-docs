# afdelaysrc

Generate a fractional delay FIR coefficients.

The resulting stream can be used with [afir](afir.md#afir) filter for filtering the audio signal.

The filter accepts the following options:

- **`delay, d`** Set the fractional delay. Default is 0.

- **`sample_rate, r`** Set the sample rate, default is 44100.

- **`nb_samples, n`** Set the number of samples per each frame. Default is 1024.

- **`taps, t`** Set the number of filter coefficients in output audio stream. Default value is 0.

- **`channel_layout, c`** Specifies the channel layout, and can be a string representing a channel layout. The default value of \<channel_layout\> is "stereo".
