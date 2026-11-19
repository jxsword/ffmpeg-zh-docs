# chorus

Add a chorus effect to the audio.

Can make a single vocal sound like a chorus, but can also be applied to instrumentation.

Chorus resembles an echo effect with a short delay, but whereas with echo the delay is constant, with chorus, it is varied using sinusoidal or triangular modulation. The modulation depth defines the range the modulated delay is played before or after the delay. Hence the delayed sound will sound slower or faster, that is the delayed sound tuned around the original one, like in a chorus where some vocals are slightly off key.

It accepts the following parameters:

| Term       | Description                                         |
|------------|-----------------------------------------------------|
| `in_gain`  | Set input gain. Default is 0.4.                     |
| `out_gain` | Set output gain. Default is 0.4.                    |
| `delays`   | Set delays. A typical delay is around 40ms to 60ms. |
| `decays`   | Set decays.                                         |
| `speeds`   | Set speeds.                                         |
| `depths`   | Set depths.                                         |

## Examples

- A single delay:

  ``` text
  chorus=0.7:0.9:55:0.4:0.25:2
  ```

- Two delays:

  ``` text
  chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|1.3
  ```

- Fuller sounding chorus with three delays:

  ``` text
  chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3
  ```
