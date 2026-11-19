# tremolo

Sinusoidal amplitude modulation.

The filter accepts the following options:

- **`f`** Modulation frequency in Hertz. Modulation frequencies in the subharmonic range (20 Hz or lower) will result in a tremolo effect. This filter may also be used as a ring modulator by specifying a modulation frequency higher than 20 Hz. Range is 0.1 - 20000.0. Default value is 5.0 Hz.

- **`d`** Depth of modulation as a percentage. Range is 0.0 - 1.0. Default value is 0.5.
