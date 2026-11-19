# extrastereo

Linearly increases the difference between left and right channels which adds some sort of "live" effect to playback.

The filter accepts the following options:

- **`m`** Sets the difference coefficient (default: 2.5). 0.0 means mono sound (average of both channels), with 1.0 sound will be unchanged, with -1.0 left and right channels will be swapped.

- **`c`** Enable clipping. By default is enabled.

## Commands

This filter supports the all above options as [commands](#commands).
