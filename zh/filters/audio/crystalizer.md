# crystalizer

Simple algorithm for audio noise sharpening.

This filter linearly increases differences between each audio sample.

The filter accepts the following options:

- **`i`** Sets the intensity of effect (default: 2.0). Must be in range between -10.0 to 0 (unchanged sound) to 10.0 (maximum effect). To inverse filtering use negative value.

- **`c`** Enable clipping. By default is enabled.

## Commands

This filter supports the all above options as [commands](#commands).
