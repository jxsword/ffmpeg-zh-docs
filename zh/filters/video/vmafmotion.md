# vmafmotion

Obtain the average VMAF motion score of a video. It is one of the component metrics of VMAF.

The obtained average motion score is printed through the logging system.

The filter accepts the following options:

- **`stats_file`** If specified, the filter will use the named file to save the motion score of each frame with respect to the previous frame. When filename equals "-" the data is sent to standard output.

Example:

``` text
ffmpeg -i ref.mpg -vf vmafmotion -f null -
```
