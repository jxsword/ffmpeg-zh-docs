# threshold

Apply threshold effect to video stream.

This filter needs four video streams to perform thresholding. First stream is stream we are filtering. Second stream is holding threshold values, third stream is holding min values, and last, fourth stream is holding max values.

The filter accepts the following option:

- **`planes`** Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.

For example if first stream pixel's component value is less then threshold value of pixel component from 2nd threshold stream, third stream value will picked, otherwise fourth stream pixel component value will be picked.

Using color source filter one can perform various types of thresholding:

## Commands

This filter supports the all options as [commands](#commands).

## Examples

- Binary threshold, using gray color as threshold:

  ``` text
  ffmpeg -i 320x240.avi -f lavfi -i color=gray -f lavfi -i color=black -f lavfi -i color=white -lavfi threshold output.avi
  ```

- Inverted binary threshold, using gray color as threshold:

  ``` text
  ffmpeg -i 320x240.avi -f lavfi -i color=gray -f lavfi -i color=white -f lavfi -i color=black -lavfi threshold output.avi
  ```

- Truncate binary threshold, using gray color as threshold:

  ``` text
  ffmpeg -i 320x240.avi -f lavfi -i color=gray -i 320x240.avi -f lavfi -i color=gray -lavfi threshold output.avi
  ```

- Threshold to zero, using gray color as threshold:

  ``` text
  ffmpeg -i 320x240.avi -f lavfi -i color=gray -f lavfi -i color=white -i 320x240.avi -lavfi threshold output.avi
  ```

- Inverted threshold to zero, using gray color as threshold:

  ``` text
  ffmpeg -i 320x240.avi -f lavfi -i color=gray -i 320x240.avi -f lavfi -i color=white -lavfi threshold output.avi
  ```
