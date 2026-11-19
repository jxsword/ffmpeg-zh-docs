# split, asplit

Split input into several identical outputs.

`asplit` works with audio input, `split` with video.

The filter accepts a single parameter which specifies the number of outputs. If unspecified, it defaults to 2.

## Examples

- Create two separate outputs from the same input:

  ``` text
  [in] split [out0][out1]
  ```

- To create 3 or more outputs, you need to specify the number of outputs, like in:

  ``` text
  [in] asplit=3 [out0][out1][out2]
  ```

- Create two separate outputs from the same input, one cropped and one padded:

  ``` text
  [in] split [splitout1][splitout2];
  [splitout1] crop=100:100:0:0    [cropout];
  [splitout2] pad=200:200:100:100 [padout];
  ```

- Create 5 copies of the input audio with `ffmpeg`:

  ``` text
  ffmpeg -i INPUT -filter_complex asplit=5 OUTPUT
  ```
