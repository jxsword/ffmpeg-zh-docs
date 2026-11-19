# atilt

Apply spectral tilt filter to audio stream.

This filter apply any spectral roll-off slope over any specified frequency band.

The filter accepts the following options:

| Term | Description |
|----|----|
| `freq` | Set central frequency of tilt in Hz. Default is 10000 Hz. |
| `slope` | Set slope direction of tilt. Default is 0. Allowed range is from -1 to 1. |
| `width` | Set width of tilt. Default is 1000. Allowed range is from 100 to 10000. |
| `order` | Set order of tilt filter. |
| `level` | Set input volume level. Allowed range is from 0 to 4. Default is 1. |

## Commands

This filter supports the all above options as [commands](#commands).
