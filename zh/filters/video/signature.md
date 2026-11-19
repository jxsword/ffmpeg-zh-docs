# signature

Calculates the MPEG-7 Video Signature. The filter can handle more than one input. In this case the matching between the inputs can be calculated additionally. The filter always passes through the first input. The signature of each stream can be written into a file.

It accepts the following options:

- **`detectmode`** Enable or disable the matching process.

  Available values are:

  - **`off`** Disable the calculation of a matching (default).

  - **`full`** Calculate the matching for the whole video and output whether the whole video matches or only parts.

  - **`fast`** Calculate only until a matching is found or the video ends. Should be faster in some cases.

- **`nb_inputs`** Set the number of inputs. The option value must be a non negative integer. Default value is 1.

- **`filename`** Set the path to which the output is written. If there is more than one input, the path must be a prototype, i.e. must contain %d or %0nd (where n is a positive integer), that will be replaced with the input number. If no filename is specified, no output will be written. This is the default.

- **`format`** Choose the output format.

  Available values are:

  | Term       | Description                                        |
  |------------|----------------------------------------------------|
  | `binary` | Use the specified binary representation (default). |
  | `xml`    | Use the specified xml representation.              |

- **`th_d`** Set threshold to detect one word as similar. The option value must be an integer greater than zero. The default value is 9000.

- **`th_dc`** Set threshold to detect all words as similar. The option value must be an integer greater than zero. The default value is 60000.

- **`th_xh`** Set threshold to detect frames as similar. The option value must be an integer greater than zero. The default value is 116.

- **`th_di`** Set the minimum length of a sequence in frames to recognize it as matching sequence. The option value must be a non negative integer value. The default value is 0.

- **`th_it`** Set the minimum relation, that matching frames to all frames must have. The option value must be a double value between 0 and 1. The default value is 0.5.

## Examples

- To calculate the signature of an input video and store it in signature.bin:

  ``` text
  ffmpeg -i input.mkv -vf signature=filename=signature.bin -map 0:v -f null -
  ```

- To detect whether two videos match and store the signatures in XML format in signature0.xml and signature1.xml:

  ``` text
  ffmpeg -i input1.mkv -i input2.mkv -filter_complex "[0:v][1:v] signature=nb_inputs=2:detectmode=full:format=xml:filename=signature%d.xml" -map :v -f null -
  ```
