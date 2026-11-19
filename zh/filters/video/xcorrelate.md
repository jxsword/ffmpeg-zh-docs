# xcorrelate

Apply normalized cross-correlation between first and second input video stream.

Second input video stream dimensions must be lower than first input video stream.

The filter accepts the following options:

- **`planes`** Set which planes to process.

- **`secondary`** Set which secondary video frames will be processed from second input video stream, can be \<first\> or \<all\>. Default is \<all\>.

The `xcorrelate` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.
