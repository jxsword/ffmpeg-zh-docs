# anoisesrc

Generate a noise audio signal.

The filter accepts the following options:

- **`sample_rate, r`** Specify the sample rate. Default value is 48000 Hz.

- **`amplitude, a`** Specify the amplitude (0.0 - 1.0) of the generated audio stream. Default value is 1.0.

- **`duration, d`** Specify the duration of the generated audio stream. Not specifying this option results in noise with an infinite length.

- **`color, colour, c`** Specify the color of noise. Available noise colors are white, pink, brown, blue, violet and velvet. Default color is white.

- **`seed, s`** Specify a value used to seed the PRNG.

- **`nb_samples, n`** Set the number of samples per each output frame, default is 1024.

- **`density`** Set the density (0.0 - 1.0) for the velvet noise generator, default is 0.05.

## Examples

- Generate 60 seconds of pink noise, with a 44.1 kHz sampling rate and an amplitude of 0.5:

  ``` text
  anoisesrc=d=60:c=pink:r=44100:a=0.5
  ```
