# rubberband

Apply time-stretching and pitch-shifting with librubberband.

To enable compilation of this filter, you need to configure FFmpeg with `--enable-librubberband`.

The filter accepts the following options:

- **`tempo`** Set tempo scale factor.

- **`pitch`** Set pitch scale factor.

- **`transients`** Set transients detector. Possible values are:

  - **\<crisp\>**

  - **\<mixed\>**

  - **\<smooth\>**

- **`detector`** Set detector. Possible values are:

  - **\<compound\>**

  - **\<percussive\>**

  - **\<soft\>**

- **`phase`** Set phase. Possible values are:

  - **\<laminar\>**

  - **\<independent\>**

- **`window`** Set processing window size. Possible values are:

  - **\<standard\>**

  - **\<short\>**

  - **\<long\>**

- **`smoothing`** Set smoothing. Possible values are:

  - **\<off\>**

  - **\<on\>**

- **`formant`** Enable formant preservation when shift pitching. Possible values are:

  - **\<shifted\>**

  - **\<preserved\>**

- **`pitchq`** Set pitch quality. Possible values are:

  - **\<quality\>**

  - **\<speed\>**

  - **\<consistency\>**

- **`channels`** Set channels. Possible values are:

  - **\<apart\>**

  - **\<together\>**

## Commands

This filter supports the following commands:

- **`tempo`** Change filter tempo scale factor. Syntax for the command is : "\<tempo\>"

- **`pitch`** Change filter pitch scale factor. Syntax for the command is : "\<pitch\>"
