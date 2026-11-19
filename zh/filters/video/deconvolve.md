# deconvolve

Apply 2D deconvolution of video stream in frequency domain using second stream as impulse.

The filter accepts the following options:

- **`planes`** Set which planes to process.

- **`impulse`** Set which impulse video frames will be processed, can be \<first\> or \<all\>. Default is \<all\>.

- **`noise`** Set noise when doing divisions. Default is \<0.0000001\>. Useful when width and height are not same and not power of 2 or if stream prior to convolving had noise.

The `deconvolve` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.
