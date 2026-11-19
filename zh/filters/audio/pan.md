# pan

Mix channels with specific gain levels. The filter accepts the output channel layout followed by a set of channels definitions.

This filter is also designed to efficiently remap the channels of an audio stream.

The filter accepts parameters of the form: "\<l\>\|\<outdef\>\|\<outdef\>\|..."

- **`l`** output channel layout or number of channels

- **`outdef`** output channel specification, of the form: "\<out_name\>=\[\<gain\>\*\]\<in_name\>\[(+-)\[\<gain\>\*\]\<in_name\>...\]"

- **`out_name`** output channel to define, either a channel name (FL, FR, etc.) or a channel number (c0, c1, etc.)

- **`gain`** multiplicative coefficient for the channel, 1 leaving the volume unchanged

- **`in_name`** input channel to use, see out_name for details; it is not possible to mix named and numbered input channels

If the '=' in a channel specification is replaced by '\<', then the gains for that specification will be renormalized so that the total is 1, thus avoiding clipping noise.

## Mixing examples

For example, if you want to down-mix from stereo to mono, but with a bigger factor for the left channel:

``` text
pan=1c|c0=0.9*c0+0.1*c1
```

A customized down-mix to stereo that works automatically for 3-, 4-, 5- and 7-channels surround:

``` text
pan=stereo| FL < FL + 0.5*FC + 0.6*BL + 0.6*SL | FR < FR + 0.5*FC + 0.6*BR + 0.6*SR
```

Note that `ffmpeg` integrates a default down-mix (and up-mix) system that should be preferred (see "-ac" option) unless you have very specific needs.

## Remapping examples

The channel remapping will be effective if, and only if:

- gain coefficients are zeroes or ones,

- only one input per channel output,

If all these conditions are satisfied, the filter will notify the user ("Pure channel mapping detected"), and use an optimized and lossless method to do the remapping.

For example, if you have a 5.1 source and want a stereo audio stream by dropping the extra channels:

``` text
pan="stereo| c0=FL | c1=FR"
```

Given the same source, you can also switch front left and front right channels and keep the input channel layout:

``` text
pan="5.1| c0=c1 | c1=c0 | c2=c2 | c3=c3 | c4=c4 | c5=c5"
```

If the input is a stereo audio stream, you can mute the front left channel (and still keep the stereo channel layout) with:

``` text
pan="stereo|c1=c1"
```

Still with a stereo audio stream input, you can copy the right channel in both front left and right:

``` text
pan="stereo| c0=FR | c1=FR"
```
