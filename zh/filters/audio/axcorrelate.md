# axcorrelate

Calculate normalized windowed cross-correlation between two input audio streams.

Resulted samples are always between -1 and 1 inclusive. If result is 1 it means two input samples are highly correlated in that selected segment. Result 0 means they are not correlated at all. If result is -1 it means two input samples are out of phase, which means they cancel each other.

The filter accepts the following options:

- **`size`** Set size of segment over which cross-correlation is calculated. Default is 256. Allowed range is from 2 to 131072.

- **`algo`** Set algorithm for cross-correlation. Can be `slow` or `fast` or `best`. Default is `best`. Fast algorithm assumes mean values over any given segment are always zero and thus need much less calculations to make. This is generally not true, but is valid for typical audio streams.

## Examples

- Calculate correlation between channels in stereo audio stream:

  ``` text
  ffmpeg -i stereo.wav -af channelsplit,axcorrelate=size=1024:algo=fast correlation.wav
  ```
