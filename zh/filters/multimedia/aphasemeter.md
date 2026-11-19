# aphasemeter

Measures phase of input audio, which is exported as metadata `lavfi.aphasemeter.phase`, representing mean phase of current audio frame. A video output can also be produced and is enabled by default. The audio is passed through as first output.

Audio will be rematrixed to stereo if it has a different channel layout. Phase value is in range `[-1, 1]` where `-1` means left and right channels are completely out of phase and `1` means channels are in phase.

The filter accepts the following options, all related to its video output:

- **`rate, r`** Set the output frame rate. Default value is `25`.

- **`size, s`** Set the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `800x400`.

- **`rc`**

- **`gc`**

- **`bc`** Specify the red, green, blue contrast. Default values are `2`, `7` and `1`. Allowed range is `[0, 255]`.

- **`mpc`** Set color which will be used for drawing median phase. If color is `none` which is default, no median phase value will be drawn.

- **`video`** Enable video output. Default is enabled.

## phasing detection

The filter also detects out of phase and mono sequences in stereo streams. It logs the sequence start, end and duration when it lasts longer or as long as the minimum set.

The filter accepts the following options for this detection:

- **`phasing`** Enable mono and out of phase detection. Default is disabled.

- **`tolerance, t`** Set phase tolerance for mono detection, in amplitude ratio. Default is `0`. Allowed range is `[0, 1]`.

- **`angle, a`** Set angle threshold for out of phase detection, in degree. Default is `170`. Allowed range is `[90, 180]`.

- **`duration, d`** Set mono or out of phase duration until notification, expressed in seconds. Default is `2`.

## Examples

- Complete example with `ffmpeg` to detect 1 second of mono with 0.001 phase tolerance:

  ``` text
  ffmpeg -i stereo.wav -af aphasemeter=video=0:phasing=1:duration=1:tolerance=0.001 -f null -
  ```
