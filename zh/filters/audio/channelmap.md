# channelmap

Remap input channels to new locations.

It accepts the following parameters:

- **`map`** Map channels from input to output. The argument is a '\|'-separated list of mappings, each in the `in_channel-out_channel` or `in_channel` form. \<in_channel\> can be either the name of the input channel (e.g. FL for front left) or its index in the input channel layout. \<out_channel\> is the name of the output channel or its index in the output channel layout. If \<out_channel\> is not given then it is implicitly an index, starting with zero and increasing by one for each mapping. Mixing different types of mappings is not allowed and will result in a parse error.

- **`channel_layout`** The channel layout of the output stream. If not specified, then filter will guess it based on the \<out_channel\> names or the number of mappings. Guessed layouts will not necessarily contain channels in the order of the mappings.

If no mapping is present, the filter will implicitly map input channels to output channels, preserving indices.

## Examples

- For example, assuming a 5.1+downmix input MOV file,

  ``` text
  ffmpeg -i in.mov -filter 'channelmap=map=DL-FL|DR-FR' out.wav
  ```

  will create an output WAV file tagged as stereo from the downmix channels of the input.

- To fix a 5.1 WAV improperly encoded in AAC's native channel order

  ``` text
  ffmpeg -i in.wav -filter 'channelmap=1|2|0|5|3|4:5.1' out.wav
  ```
