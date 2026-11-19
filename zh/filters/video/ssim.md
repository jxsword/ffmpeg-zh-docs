# ssim

Obtain the SSIM (Structural SImilarity Metric) between two input videos.

This filter takes in input two input videos, the first input is considered the "main" source and is passed unchanged to the output. The second input is used as a "reference" video for computing the SSIM.

Both video inputs must have the same resolution and pixel format for this filter to work correctly. Also it assumes that both inputs have the same number of frames, which are compared one by one.

The filter stores the calculated SSIM of each frame.

The description of the accepted parameters follows.

- **`stats_file, f`** If specified the filter will use the named file to save the SSIM of each individual frame. When filename equals "-" the data is sent to standard output.

The file printed if \<stats_file\> is selected, contains a sequence of key/value pairs of the form \<key\>:\<value\> for each compared couple of frames.

A description of each shown parameter follows:

| Term | Description |
|----|----|
| `n` | sequential number of the input frame, starting from 1 |
| `Y, U, V, R, G, B` | SSIM of the compared frames for the component specified by the suffix. |
| `All` | SSIM of the compared frames for the whole frame. |
| `dB` | Same as above but in dB representation. |

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Examples

- For example:

  ``` text
  movie=ref_movie.mpg, setpts=PTS-STARTPTS [main];
  [main][ref] ssim="stats_file=stats.log" [out]
  ```

  On this example the input file being processed is compared with the reference file `ref_movie.mpg`. The SSIM of each individual frame is stored in `stats.log`.

- Another example with both psnr and ssim at same time:

  ``` text
  ffmpeg -i main.mpg -i ref.mpg -lavfi  "ssim;[0:v][1:v]psnr" -f null -
  ```

- Another example with different containers:

  ``` text
  ffmpeg -i main.mpg -i ref.mkv -lavfi  "[0:v]settb=AVTB,setpts=PTS-STARTPTS[main];[1:v]settb=AVTB,setpts=PTS-STARTPTS[ref];[main][ref]ssim" -f null -
  ```
