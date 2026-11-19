# amix

Mixes multiple audio inputs into a single output.

Note that this filter only supports float samples (the \<amerge\> and \<pan\> audio filters support many formats). If the \<amix\> input has integer samples then [aresample](aresample.md#aresample) will be automatically inserted to perform the conversion to float samples.

It accepts the following parameters:

- **`inputs`** The number of inputs. If unspecified, it defaults to 2.

- **`duration`** How to determine the end-of-stream.

  | Term       | Description                                  |
  |------------|----------------------------------------------|
  | `longest`  | The duration of the longest input. (default) |
  | `shortest` | The duration of the shortest input.          |
  | `first`    | The duration of the first input.             |

- **`dropout_transition`** The transition time, in seconds, for volume renormalization when an input stream ends. The default value is 2 seconds.

- **`weights`** Specify weight of each input audio stream as a sequence of numbers separated by a space. If fewer weights are specified compared to number of inputs, the last weight is assigned to the remaining inputs. Default weight for each input is 1.

- **`normalize`** Always scale inputs instead of only doing summation of samples. Beware of heavy clipping if inputs are not normalized prior or after filtering by this filter if this option is disabled. By default is enabled.

## Examples

- This will mix 3 input audio streams to a single output with the same duration as the first input and a dropout transition time of 3 seconds:

  ``` text
  ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 -filter_complex amix=inputs=3:duration=first:dropout_transition=3 OUTPUT
  ```

- This will mix one vocal and one music input audio stream to a single output with the same duration as the longest input. The music will have quarter the weight as the vocals, and the inputs are not normalized:

  ``` text
  ffmpeg -i VOCALS -i MUSIC -filter_complex amix=inputs=2:duration=longest:dropout_transition=0:weights="1 0.25":normalize=0 OUTPUT
  ```

## Commands

This filter supports the following commands:

- **`weights`**

- **`normalize`** Syntax is same as option with same name.
