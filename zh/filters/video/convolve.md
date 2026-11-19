# convolve

Apply 2D convolution of video stream in frequency domain using second stream as impulse.

The filter accepts the following options:

- **`planes`** Set which planes to process.

- **`impulse`** Set which impulse video frames will be processed, can be \<first\> or \<all\>. Default is \<all\>.

The `convolve` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.
