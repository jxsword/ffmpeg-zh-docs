# loop

Loop video frames.

The filter accepts the following options:

- **`loop`** Set the number of loops. Setting this value to -1 will result in infinite loops. Default is 0.

- **`size`** Set maximal size in number of frames. Default is 0.

- **`start`** Set first frame of loop. Default is 0.

- **`time`** Set the time of loop start in seconds. Only used if option named \<start\> is set to `-1`.

## Examples

- Loop single first frame infinitely:

  ``` text
  loop=loop=-1:size=1:start=0
  ```

- Loop single first frame 10 times:

  ``` text
  loop=loop=10:size=1:start=0
  ```

- Loop 10 first frames 5 times:

  ``` text
  loop=loop=5:size=10:start=0
  ```
