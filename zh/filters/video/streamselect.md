# streamselect, astreamselect

Select video or audio streams.

The filter accepts the following options:

| Term     | Description                            |
|----------|----------------------------------------|
| `inputs` | Set number of inputs. Default is 2.    |
| `map`    | Set input indexes to remap to outputs. |

## Commands

The `streamselect` and `astreamselect` filter supports the following commands:

| Term  | Description                            |
|-------|----------------------------------------|
| `map` | Set input indexes to remap to outputs. |

## Examples

- Select first 5 seconds 1st stream and rest of time 2nd stream:

  ``` text
  sendcmd='5.0 streamselect map 1',streamselect=inputs=2:map=0
  ```

- Same as above, but for audio:

  ``` text
  asendcmd='5.0 astreamselect map 1',astreamselect=inputs=2:map=0
  ```
