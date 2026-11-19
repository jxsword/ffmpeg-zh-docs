# compand

Compress or expand the audio's dynamic range.

It accepts the following parameters:

- **`attacks`**

- **`decays`** A list of times in seconds for each channel over which the instantaneous level of the input signal is averaged to determine its volume. \<attacks\> refers to increase of volume and \<decays\> refers to decrease of volume. For most situations, the attack time (response to the audio getting louder) should be shorter than the decay time, because the human ear is more sensitive to sudden loud audio than sudden soft audio. A typical value for attack is 0.3 seconds and a typical value for decay is 0.8 seconds. If specified number of attacks & decays is lower than number of channels, the last set attack/decay will be used for all remaining channels.

- **`points`** A list of points for the transfer function, specified in dB relative to the maximum possible signal amplitude. Each key points list must be defined using the following syntax: `x0/y0|x1/y1|x2/y2|....` or `x0/y0 x1/y1 x2/y2 ....`

  The input values must be in strictly increasing order but the transfer function does not have to be monotonically rising. The point `0/0` is assumed but may be overridden (by `0/out-dBn`). Typical values for the transfer function are `-70/-70|-60/-20|1/0`.

- **`soft-knee`** Set the curve radius in dB for all joints. It defaults to 0.01.

- **`gain`** Set the additional gain in dB to be applied at all points on the transfer function. This allows for easy adjustment of the overall gain. It defaults to 0.

- **`volume`** Set an initial volume, in dB, to be assumed for each channel when filtering starts. This permits the user to supply a nominal level initially, so that, for example, a very large gain is not applied to initial signal levels before the companding has begun to operate. A typical value for audio which is initially quiet is -90 dB. It defaults to 0.

- **`delay`** Set a delay, in seconds. The input audio is analyzed immediately, but audio is delayed before being fed to the volume adjuster. Specifying a delay approximately equal to the attack/decay times allows the filter to effectively operate in predictive rather than reactive mode. It defaults to 0.

## Examples

- Make music with both quiet and loud passages suitable for listening to in a noisy environment:

  ``` text
  compand=.3|.3:1|1:-90/-60|-60/-40|-40/-30|-20/-20:6:0:-90:0.2
  ```

  Another example for audio with whisper and explosion parts:

  ``` text
  compand=0|0:1|1:-90/-900|-70/-70|-30/-9|0/-3:6:0:0:0
  ```

- A noise gate for when the noise is at a lower level than the signal:

  ``` text
  compand=.1|.1:.2|.2:-900/-900|-50.1/-900|-50/-50:.01:0:-90:.1
  ```

- Here is another noise gate, this time for when the noise is at a higher level than the signal (making it, in some ways, similar to squelch):

  ``` text
  compand=.1|.1:.1|.1:-45.1/-45.1|-45/-900|0/-900:.01:45:-90:.1
  ```

- 2:1 compression starting at -6dB:

  ``` text
  compand=points=-80/-80|-6/-6|0/-3.8|20/3.5
  ```

- 2:1 compression starting at -9dB:

  ``` text
  compand=points=-80/-80|-9/-9|0/-5.3|20/2.9
  ```

- 2:1 compression starting at -12dB:

  ``` text
  compand=points=-80/-80|-12/-12|0/-6.8|20/1.9
  ```

- 2:1 compression starting at -18dB:

  ``` text
  compand=points=-80/-80|-18/-18|0/-9.8|20/0.7
  ```

- 3:1 compression starting at -15dB:

  ``` text
  compand=points=-80/-80|-15/-15|0/-10.8|20/-5.2
  ```

- Compressor/Gate:

  ``` text
  compand=points=-80/-105|-62/-80|-15.4/-15.4|0/-12|20/-7.6
  ```

- Expander:

  ``` text
  compand=attacks=0:points=-80/-169|-54/-80|-49.5/-64.6|-41.1/-41.1|-25.8/-15|-10.8/-4.5|0/0|20/8.3
  ```

- Hard limiter at -6dB:

  ``` text
  compand=attacks=0:points=-80/-80|-6/-6|20/-6
  ```

- Hard limiter at -12dB:

  ``` text
  compand=attacks=0:points=-80/-80|-12/-12|20/-12
  ```

- Hard noise gate at -35 dB:

  ``` text
  compand=attacks=0:points=-80/-115|-35.1/-80|-35/-35|20/20
  ```

- Soft limiter:

  ``` text
  compand=attacks=0:points=-80/-80|-12.4/-12.4|-6/-8|0/-6.8|20/-2.8
  ```
