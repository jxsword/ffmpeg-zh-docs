# apulsator

Audio pulsator is something between an autopanner and a tremolo. But it can produce funny stereo effects as well. Pulsator changes the volume of the left and right channel based on a LFO (low frequency oscillator) with different waveforms and shifted phases. This filter have the ability to define an offset between left and right channel. An offset of 0 means that both LFO shapes match each other. The left and right channel are altered equally - a conventional tremolo. An offset of 50% means that the shape of the right channel is exactly shifted in phase (or moved backwards about half of the frequency) - pulsator acts as an autopanner. At 1 both curves match again. Every setting in between moves the phase shift gapless between all stages and produces some "bypassing" sounds with sine and triangle waveforms. The more you set the offset near 1 (starting from the 0.5) the faster the signal passes from the left to the right speaker.

The filter accepts the following options:

- **`level_in`** Set input gain. By default it is 1. Range is \[0.015625 - 64\].

- **`level_out`** Set output gain. By default it is 1. Range is \[0.015625 - 64\].

- **`mode`** Set waveform shape the LFO will use. Can be one of: sine, triangle, square, sawup or sawdown. Default is sine.

- **`amount`** Set modulation. Define how much of original signal is affected by the LFO.

- **`offset_l`** Set left channel offset. Default is 0. Allowed range is \[0 - 1\].

- **`offset_r`** Set right channel offset. Default is 0.5. Allowed range is \[0 - 1\].

- **`width`** Set pulse width. Default is 1. Allowed range is \[0 - 2\].

- **`timing`** Set possible timing mode. Can be one of: bpm, ms or hz. Default is hz.

- **`bpm`** Set bpm. Default is 120. Allowed range is \[30 - 300\]. Only used if timing is set to bpm.

- **`ms`** Set ms. Default is 500. Allowed range is \[10 - 2000\]. Only used if timing is set to ms.

- **`hz`** Set frequency in Hz. Default is 2. Allowed range is \[0.01 - 100\]. Only used if timing is set to hz.
