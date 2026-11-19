# amerge

Merge two or more audio streams into a single multi-channel stream.

All inputs must have the same sample rate, and format.

If inputs do not have the same duration, the output will stop with the shortest.

The filter accepts the following options:

- **`inputs`** Set the number of inputs. Default is 2.

- **`layout_mode`** This option controls how the output channel layout is determined and if the audio channels are reordered during merge.

  - **`legacy`** This is the mode how the filter behaved historically so it is the default.

    If the channel layouts of the inputs are known and disjoint, and therefore compatible, the channel layout of the output will be set accordingly and the channels will be reordered as necessary. If the channel layouts of the inputs are not disjoint, some of them are unknown, or they are using special channel layouts, such as ambisonics, the output will have all the channels of the first input then all the channels of the second input, in that order, and the channel layout of the output will be the default value corresponding to the total number of channels.

    For example, if the first input is in 2.1 (FL+FR+LF) and the second input is FC+BL+BR, then the output will be in 5.1, with the channels in the following order: a1, a2, b1, a3, b2, b3 (a1 is the first channel of the first input, b1 is the first channel of the second input).

    On the other hand, if both input are in stereo, the output channels will be in the default order: a1, a2, b1, b2, and the channel layout will be arbitrarily set to 4.0, which may or may not be the expected value.

  - **`reset`** This mode ignores the input channel layouts and does no channel reordering. The output will have all the channels of the first input, then all the channels of the second input, in that order, and so on.

    The output channel layout will only specify the total channel count.

  - **`normal`** This mode keeps channel name and designation information from the input channels and does no channel reordering. The output will have all the channels of the first input, then all the channels of the second input, in that order, and so on.

## Examples

- Merge two mono files into a stereo stream:

  ``` text
  amovie=left.wav [l] ; amovie=right.mp3 [r] ; [l] [r] amerge
  ```

- Multiple merges assuming 1 video stream and 6 audio streams in `input.mkv`:

  ``` text
  ffmpeg -i input.mkv -filter_complex "[0:1][0:2][0:3][0:4][0:5][0:6] amerge=inputs=6" -c:a pcm_s16le output.mkv
  ```
