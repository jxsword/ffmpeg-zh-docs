# tmix

Mix successive video frames.

A description of the accepted options follows.

- **`frames`** The number of successive frames to mix. If unspecified, it defaults to 3.

- **`weights`** Specify weight of each input video frame. Each weight is separated by space. If number of weights is smaller than number of \<frames\> last specified weight will be used for all remaining unset weights.

- **`scale`** Specify scale, if it is set it will be multiplied with sum of each weight multiplied with pixel values to give final destination pixel value. By default \<scale\> is auto scaled to sum of weights.

- **`planes`** Set which planes to filter. Default is all. Allowed range is from 0 to 15.

## Examples

- Average 7 successive frames:

  ``` text
  tmix=frames=7:weights="1 1 1 1 1 1 1"
  ```

- Apply simple temporal convolution:

  ``` text
  tmix=frames=3:weights="-1 3 -1"
  ```

- Similar as above but only showing temporal differences:

  ``` text
  tmix=frames=3:weights="-1 2 -1":scale=1
  ```

## Commands

This filter supports the following commands:

- **`weights`**

- **`scale`**

- **`planes`** Syntax is same as option with same name.
