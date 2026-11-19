# shuffleframes

Reorder and/or duplicate and/or drop video frames.

It accepts the following parameters:

- **`mapping`** Set the destination indexes of input frames. This is space or '\|' separated list of indexes that maps input frames to output frames. Number of indexes also sets maximal value that each index may have. '-1' index have special meaning and that is to drop frame.

The first frame has the index 0. The default is to keep the input unchanged.

## Examples

- Swap second and third frame of every three frames of the input:

  ``` text
  ffmpeg -i INPUT -vf "shuffleframes=0 2 1" OUTPUT
  ```

- Swap 10th and 1st frame of every ten frames of the input:

  ``` text
  ffmpeg -i INPUT -vf "shuffleframes=9 1 2 3 4 5 6 7 8 0" OUTPUT
  ```
