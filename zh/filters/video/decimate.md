# decimate

Drop duplicated frames at regular intervals.

The filter accepts the following options:

- **`cycle`** Set the number of frames from which one will be dropped. Setting this to \<N\> means one frame in every batch of \<N\> frames will be dropped. Default is `5`.

- **`dupthresh`** Set the threshold for duplicate detection. If the difference metric for a frame is less than or equal to this value, then it is declared as duplicate. Default is `1.1`

- **`scthresh`** Set scene change threshold. Default is `15`.

- **`blockx`**

- **`blocky`** Set the size of the x and y-axis blocks used during metric calculations. Larger blocks give better noise suppression, but also give worse detection of small movements. Must be a power of two. Default is `32`.

- **`ppsrc`** Mark main input as a pre-processed input and activate clean source input stream. This allows the input to be pre-processed with various filters to help the metrics calculation while keeping the frame selection lossless. When set to `1`, the first stream is for the pre-processed input, and the second stream is the clean source from where the kept frames are chosen. Default is `0`.

- **`chroma`** Set whether or not chroma is considered in the metric calculations. Default is `1`.

- **`mixed`** Set whether or not the input only partially contains content to be decimated. Default is `false`. If enabled video output stream will be in variable frame rate.
