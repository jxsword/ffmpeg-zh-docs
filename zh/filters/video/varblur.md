# varblur

Apply variable blur filter by using 2nd video stream to set blur radius. The 2nd stream must have the same dimensions.

This filter accepts the following options:

| Term | Description |
|----|----|
| `min_r` | Set min allowed radius. Allowed range is from 0 to 254. Default is 0. |
| `max_r` | Set max allowed radius. Allowed range is from 1 to 255. Default is 8. |
| `planes` | Set which planes to process. By default, all are used. |

The `varblur` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Commands

This filter supports all the above options as [commands](#commands).
