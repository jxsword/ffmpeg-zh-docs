# mix

Mix several video input streams into one video stream.

A description of the accepted options follows.

- **`inputs`** The number of inputs. If unspecified, it defaults to 2.

- **`weights`** Specify weight of each input video stream as sequence. Each weight is separated by space. If number of weights is smaller than number of \<frames\> last specified weight will be used for all remaining unset weights.

- **`scale`** Specify scale, if it is set it will be multiplied with sum of each weight multiplied with pixel values to give final destination pixel value. By default \<scale\> is auto scaled to sum of weights.

- **`planes`** Set which planes to filter. Default is all. Allowed range is from 0 to 15.

- **`duration`** Specify how end of stream is determined.

  | Term         | Description                                  |
  |--------------|----------------------------------------------|
  | `longest`  | The duration of the longest input. (default) |
  | `shortest` | The duration of the shortest input.          |
  | `first`    | The duration of the first input.             |

## Commands

This filter supports the following commands:

- **`weights`**

- **`scale`**

- **`planes`** Syntax is same as option with same name.
