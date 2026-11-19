# anequalizer

High-order parametric multiband equalizer for each channel.

It accepts the following parameters:

- **`params`** This option string is in format: "c\<chn\> f=\<cf\> w=\<w\> g=\<g\> t=\<f\> \| ..." Each equalizer band is separated by '\|'.

  - **`chn`** Set channel number to which equalization will be applied. If input doesn't have that channel the entry is ignored.

  - **`f`** Set central frequency for band. If input doesn't have that frequency the entry is ignored.

  - **`w`** Set band width in Hertz.

  - **`g`** Set band gain in dB.

  - **`t`** Set filter type for band, optional, can be:

    | Term  | Description                   |
    |-------|-------------------------------|
    | `0` | Butterworth, this is default. |
    | `1` | Chebyshev type 1.             |
    | `2` | Chebyshev type 2.             |

- **`curves`** With this option activated frequency response of anequalizer is displayed in video stream.

- **`size`** Set video stream size. Only useful if curves option is activated.

- **`mgain`** Set max gain that will be displayed. Only useful if curves option is activated. Setting this to a reasonable value makes it possible to display gain which is derived from neighbour bands which are too close to each other and thus produce higher gain when both are activated.

- **`fscale`** Set frequency scale used to draw frequency response in video output. Can be linear or logarithmic. Default is logarithmic.

- **`colors`** Set color for each channel curve which is going to be displayed in video stream. This is list of color names separated by space or by '\|'. Unrecognised or missing colors will be replaced by white color.

## Examples

- Lower gain by 10 of central frequency 200Hz and width 100 Hz for first 2 channels using Chebyshev type 1 filter:

  ``` text
  anequalizer=c0 f=200 w=100 g=-10 t=1|c1 f=200 w=100 g=-10 t=1
  ```

## Commands

This filter supports the following commands:

- **`change`** Alter existing filter parameters. Syntax for the commands is : "\<fN\>\|f=\<freq\>\|w=\<width\>\|g=\<gain\>"

  \<fN\> is existing filter number, starting from 0, if no such filter is available error is returned. \<freq\> set new frequency parameter. \<width\> set new width parameter in Hertz. \<gain\> set new gain parameter in dB.

  Full filter invocation with asendcmd may look like this: asendcmd=c='4.0 anequalizer change 0\|f=200\|w=50\|g=1',anequalizer=...
