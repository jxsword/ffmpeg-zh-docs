# join

Join multiple input streams into one multi-channel stream.

It accepts the following parameters:

- **`inputs`** The number of input streams. It defaults to 2.

- **`channel_layout`** The desired output channel layout. It defaults to stereo.

- **`map`** Map channels from inputs to output. The argument is a '\|'-separated list of mappings, each in the `input_idx.in_channel-out_channel` form. \<input_idx\> is the 0-based index of the input stream. \<in_channel\> can be either the name of the input channel (e.g. FL for front left) or its index in the specified input stream. \<out_channel\> is the name of the output channel.

The filter will attempt to guess the mappings when they are not specified explicitly. It does so by first trying to find an unused matching input channel and if that fails it picks the first unused input channel.

Join 3 inputs (with properly set channel layouts):

``` text
ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 -filter_complex join=inputs=3 OUTPUT
```

Build a 5.1 output from 6 single-channel streams:

``` text
ffmpeg -i fl -i fr -i fc -i sl -i sr -i lfe -filter_complex
'join=inputs=6:channel_layout=5.1:map=0.0-FL|1.0-FR|2.0-FC|3.0-SL|4.0-SR|5.0-LFE'
out
```
