# realtime, arealtime

Slow down filtering to match real time approximately.

These filters will pause the filtering for a variable amount of time to match the output rate with the input timestamps. They are similar to the `re` option to `ffmpeg`.

They accept the following options:

- **`limit`** Time limit for the pauses. Any pause longer than that will be considered a timestamp discontinuity and reset the timer. Default is 2 seconds.

- **`speed`** Speed factor for processing. The value must be a float larger than zero. Values larger than 1.0 will result in faster than realtime processing, smaller will slow processing down. The \<limit\> is automatically adapted accordingly. Default is 1.0.

  A processing speed faster than what is possible without these filters cannot be achieved.

## Commands

Both filters supports the all above options as [commands](#commands).
