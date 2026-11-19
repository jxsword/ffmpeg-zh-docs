# aecho

Apply echoing to the input audio.

Echoes are reflected sound and can occur naturally amongst mountains (and sometimes large buildings) when talking or shouting; digital echo effects emulate this behaviour and are often used to help fill out the sound of a single instrument or vocal. The time difference between the original signal and the reflection is the `delay`, and the loudness of the reflected signal is the `decay`. Multiple echoes can have different delays and decays.

A description of the accepted parameters follows.

- **`in_gain`** Set input gain of reflected signal. Default is `0.6`.

- **`out_gain`** Set output gain of reflected signal. Default is `0.3`.

- **`delays`** Set list of time intervals in milliseconds between original signal and reflections separated by '\|'. Allowed range for each `delay` is `(0 - 90000.0]`. Default is `1000`.

- **`decays`** Set list of loudness of reflected signals separated by '\|'. Allowed range for each `decay` is `(0 - 1.0]`. Default is `0.5`.

## Examples

- Make it sound as if there are twice as many instruments as are actually playing:

  ``` text
  aecho=0.8:0.88:60:0.4
  ```

- If delay is very short, then it sounds like a (metallic) robot playing music:

  ``` text
  aecho=0.8:0.88:6:0.4
  ```

- A longer delay will sound like an open air concert in the mountains:

  ``` text
  aecho=0.8:0.9:1000:0.3
  ```

- Same as above but with one more mountain:

  ``` text
  aecho=0.8:0.9:1000|1800:0.3|0.25
  ```
