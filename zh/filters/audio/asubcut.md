# asubcut

Cut subwoofer frequencies.

This filter allows to set custom, steeper roll off than highpass filter, and thus is able to more attenuate frequency content in stop-band.

The filter accepts the following options:

| Term | Description |
|----|----|
| `cutoff` | Set cutoff frequency in Hertz. Allowed range is 2 to 200. Default value is 20. |
| `order` | Set filter order. Available values are from 3 to 20. Default value is 10. |
| `level` | Set input gain level. Allowed range is from 0 to 1. Default value is 1. |

## Commands

This filter supports the all above options as [commands](#commands).
