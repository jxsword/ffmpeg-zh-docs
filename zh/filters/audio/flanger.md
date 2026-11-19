# flanger

Apply a flanging effect to the audio.

The filter accepts the following options:

- **`delay`** Set base delay in milliseconds. Range from 0 to 30. Default value is 0.

- **`depth`** Set added sweep delay in milliseconds. Range from 0 to 10. Default value is 2.

- **`regen`** Set percentage regeneration (delayed signal feedback). Range from -95 to 95. Default value is 0.

- **`width`** Set percentage of delayed signal mixed with original. Range from 0 to 100. Default value is 71.

- **`speed`** Set sweeps per second (Hz). Range from 0.1 to 10. Default value is 0.5.

- **`shape`** Set swept wave shape, can be \<triangular\> or \<sinusoidal\>. Default value is \<sinusoidal\>.

- **`phase`** Set swept wave percentage-shift for multi channel. Range from 0 to 100. Default value is 25.

- **`interp`** Set delay-line interpolation, \<linear\> or \<quadratic\>. Default is \<linear\>.
