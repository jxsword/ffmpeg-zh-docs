# bench, abench

Benchmark part of a filtergraph.

The filter accepts the following options:

- **`action`** Start or stop a timer.

  Available values are:

  - **`start`** Get the current time, set it as frame metadata (using the key `lavfi.bench.start_time`), and forward the frame to the next filter.

  - **`stop`** Get the current time and fetch the `lavfi.bench.start_time` metadata from the input frame metadata to get the time difference. Time difference, average, maximum and minimum time (respectively `t`, `avg`, `max` and `min`) are then printed. The timestamps are expressed in seconds.

## Examples

- Benchmark [selectivecolor](../video/selectivecolor.md#selectivecolor) filter:

  ``` text
  bench=start,selectivecolor=reds=-.2 .12 -.49,bench=stop
  ```
