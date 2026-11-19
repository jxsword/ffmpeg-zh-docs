# psnr

Obtain the average, maximum and minimum PSNR (Peak Signal to Noise Ratio) between two input videos.

This filter takes in input two input videos, the first input is considered the "main" source and is passed unchanged to the output. The second input is used as a "reference" video for computing the PSNR.

Both video inputs must have the same resolution and pixel format for this filter to work correctly. Also it assumes that both inputs have the same number of frames, which are compared one by one.

The obtained average PSNR is printed through the logging system.

The filter stores the accumulated MSE (mean squared error) of each frame, and at the end of the processing it is averaged across all frames equally, and the following formula is applied to obtain the PSNR:

``` text
PSNR = 10*log10(MAX^2/MSE)
```

Where MAX is the average of the maximum values of each component of the image.

The description of the accepted parameters follows.

- **`stats_file, f`** If specified the filter will use the named file to save the PSNR of each individual frame. When filename equals "-" the data is sent to standard output.

- **`stats_version`** Specifies which version of the stats file format to use. Details of each format are written below. Default value is 1.

- **`output_max`** Determines whether the max value is output to the stats log. Default value is 0. Requires stats_version \>= 2. If this is set and stats_version \< 2, the filter will return an error.

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

The file printed if \<stats_file\> is selected, contains a sequence of key/value pairs of the form \<key\>:\<value\> for each compared couple of frames.

If a \<stats_version\> greater than 1 is specified, a header line precedes the list of per-frame-pair stats, with key value pairs following the frame format with the following parameters:

- **`psnr_log_version`** The version of the log file format. Will match \<stats_version\>.

- **`fields`** A comma separated list of the per-frame-pair parameters included in the log.

A description of each shown per-frame-pair parameter follows:

- **`n`** sequential number of the input frame, starting from 1

- **`mse_avg`** Mean Square Error pixel-by-pixel average difference of the compared frames, averaged over all the image components.

- **`mse_y, mse_u, mse_v, mse_r, mse_g, mse_b, mse_a`** Mean Square Error pixel-by-pixel average difference of the compared frames for the component specified by the suffix.

- **`psnr_y, psnr_u, psnr_v, psnr_r, psnr_g, psnr_b, psnr_a`** Peak Signal to Noise ratio of the compared frames for the component specified by the suffix.

- **`max_avg, max_y, max_u, max_v`** Maximum allowed value for each channel, and average over all channels.

## Examples

- For example:

  ``` text
  movie=ref_movie.mpg, setpts=PTS-STARTPTS [main];
  [main][ref] psnr="stats_file=stats.log" [out]
  ```

  On this example the input file being processed is compared with the reference file `ref_movie.mpg`. The PSNR of each individual frame is stored in `stats.log`.

- Another example with different containers:

  ``` text
  ffmpeg -i main.mpg -i ref.mkv -lavfi  "[0:v]settb=AVTB,setpts=PTS-STARTPTS[main];[1:v]settb=AVTB,setpts=PTS-STARTPTS[ref];[main][ref]psnr" -f null -
  ```
