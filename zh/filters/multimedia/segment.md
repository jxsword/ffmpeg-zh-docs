# segment, asegment

Split single input stream into multiple streams.

This filter does opposite of concat filters.

`segment` works on video frames, `asegment` on audio samples.

This filter accepts the following options:

- **`timestamps`** Timestamps of output segments separated by '\|'. The first segment will run from the beginning of the input stream. The last segment will run until the end of the input stream

- **`frames, samples`** Exact frame/sample count to split the segments.

In all cases, prefixing an each segment with '+' will make it relative to the previous segment.

## Examples

- Split input audio stream into three output audio streams, starting at start of input audio stream and storing that in 1st output audio stream, then following at 60th second and storing than in 2nd output audio stream, and last after 150th second of input audio stream store in 3rd output audio stream:

  ``` text
  asegment=timestamps="60|150"
  ```
