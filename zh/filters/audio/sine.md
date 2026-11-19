# sine

Generate an audio signal made of a sine wave with amplitude 1/8.

The audio signal is bit-exact.

The filter accepts the following options:

- **`frequency, f`** Set the carrier frequency. Default is 440 Hz.

- **`beep_factor, b`** Enable a periodic beep every second with frequency \<beep_factor\> times the carrier frequency. Default is 0, meaning the beep is disabled.

- **`sample_rate, r`** Specify the sample rate, default is 44100.

- **`duration, d`** Specify the duration of the generated audio stream.

- **`samples_per_frame`** Set the number of samples per output frame.

  The expression can contain the following constants:

  - **`n`** The (sequential) number of the output audio frame, starting from 0.

  - **`pts`** The PTS (Presentation TimeStamp) of the output audio frame, expressed in \<TB\> units.

  - **`t`** The PTS of the output audio frame, expressed in seconds.

  - **`TB`** The timebase of the output audio frames.

  Default is `1024`.

## Examples

- Generate a simple 440 Hz sine wave:

  ``` text
  sine
  ```

- Generate a 220 Hz sine wave with a 880 Hz beep each second, for 5 seconds:

  ``` text
  sine=220:4:d=5
  sine=f=220:b=4:d=5
  sine=frequency=220:beep_factor=4:duration=5
  ```

- Generate a 1 kHz sine wave following `1602,1601,1602,1601,1602` NTSC pattern:

  ``` c
  sine=1000:samples_per_frame='st(0,mod(n,5)); 1602-not(not(eq(ld(0),1)+eq(ld(0),3)))'
  ```
