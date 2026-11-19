# avsynctest

Generate an Audio/Video Sync Test.

Generated stream periodically shows flash video frame and emits beep in audio. Useful to inspect A/V sync issues.

It accepts the following options:

- **`size, s`** Set output video size. Default value is `hd720`.

- **`framerate, fr`** Set output video frame rate. Default value is `30`.

- **`samplerate, sr`** Set output audio sample rate. Default value is `44100`.

- **`amplitude, a`** Set output audio beep amplitude. Default value is `0.7`.

- **`period, p`** Set output audio beep period in seconds. Default value is `3`.

- **`delay, dl`** Set output video flash delay in number of frames. Default value is `0`.

- **`cycle, c`** Enable cycling of video delays, by default is disabled.

- **`duration, d`** Set stream output duration. By default duration is unlimited.

- **`fg, bg, ag`** Set foreground/background/additional color.

## Commands

This source supports the some above options as [commands](#commands).
