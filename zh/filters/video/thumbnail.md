# thumbnail

Select the most representative frame in a given sequence of consecutive frames.

The filter accepts the following options:

- **`n`** Set the frames batch size to analyze; in a set of \<n\> frames, the filter will pick one of them, and then handle the next batch of \<n\> frames until the end. Default is `100`.

- **`log`** Set the log level to display picked frame stats. Default is `info`.

Since the filter keeps track of the whole frames sequence, a bigger \<n\> value will result in a higher memory usage, so a high value is not recommended.

## Examples

- Extract one picture each 50 frames:

  ``` text
  thumbnail=50
  ```

- Complete example of a thumbnail creation with `ffmpeg`:

  ``` text
  ffmpeg -i in.avi -vf thumbnail,scale=300:200 -frames:v 1 out.png
  ```
