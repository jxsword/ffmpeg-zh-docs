# sidechaincompress

This filter acts like normal compressor but has the ability to compress detected signal using second input signal. It needs two input streams and returns one output stream. First input stream will be processed depending on second stream signal. The filtered signal then can be filtered with other filters in later stages of processing. See [pan](pan.md#pan) and [amerge](amerge.md#amerge) filter.

The filter accepts the following options:

- **`level_in`** Set input gain. Default is 1. Range is between 0.015625 and 64.

- **`mode`** Set mode of compressor operation. Can be `upward` or `downward`. Default is `downward`.

- **`threshold`** If a signal of second stream raises above this level it will affect the gain reduction of first stream. By default is 0.125. Range is between 0.00097563 and 1.

- **`ratio`** Set a ratio about which the signal is reduced. 1:2 means that if the level raised 4dB above the threshold, it will be only 2dB above after the reduction. Default is 2. Range is between 1 and 20.

- **`attack`** Amount of milliseconds the signal has to rise above the threshold before gain reduction starts. Default is 20. Range is between 0.01 and 2000.

- **`release`** Amount of milliseconds the signal has to fall below the threshold before reduction is decreased again. Default is 250. Range is between 0.01 and 9000.

- **`makeup`** Set the amount by how much signal will be amplified after processing. Default is 1. Range is from 1 to 64.

- **`knee`** Curve the sharp knee around the threshold to enter gain reduction more softly. Default is 2.82843. Range is between 1 and 8.

- **`link`** Choose if the `average` level between all channels of side-chain stream or the louder(`maximum`) channel of side-chain stream affects the reduction. Default is `average`.

- **`detection`** Should the exact signal be taken in case of `peak` or an RMS one in case of `rms`. Default is `rms` which is mainly smoother.

- **`level_sc`** Set sidechain gain. Default is 1. Range is between 0.015625 and 64.

- **`mix`** How much to use compressed signal in output. Default is 1. Range is between 0 and 1.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Full ffmpeg example taking 2 audio inputs, 1st input to be compressed depending on the signal of 2nd input and later compressed signal to be merged with 2nd input:

  ``` text
  ffmpeg -i main.flac -i sidechain.flac -filter_complex "[1:a]asplit=2[sc][mix];[0:a][sc]sidechaincompress[compr];[compr][mix]amerge"
  ```
