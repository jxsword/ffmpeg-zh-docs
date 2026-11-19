# sinc

Generate a sinc kaiser-windowed low-pass, high-pass, band-pass, or band-reject FIR coefficients.

The resulting stream can be used with [afir](afir.md#afir) filter for filtering the audio signal.

The filter accepts the following options:

- **`sample_rate, r`** Set sample rate, default is 44100.

- **`nb_samples, n`** Set number of samples per each frame. Default is 1024.

- **`hp`** Set high-pass frequency. Default is 0.

- **`lp`** Set low-pass frequency. Default is 0. If high-pass frequency is lower than low-pass frequency and low-pass frequency is higher than 0 then filter will create band-pass filter coefficients, otherwise band-reject filter coefficients.

- **`phase`** Set filter phase response. Default is 50. Allowed range is from 0 to 100.

- **`beta`** Set Kaiser window beta.

- **`att`** Set stop-band attenuation. Default is 120dB, allowed range is from 40 to 180 dB.

- **`round`** Enable rounding, by default is disabled.

- **`hptaps`** Set number of taps for high-pass filter.

- **`lptaps`** Set number of taps for low-pass filter.
