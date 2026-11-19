# fade

Apply a fade-in/out effect to the input video.

It accepts the following parameters:

- **`type, t`** The effect type can be either "in" for a fade-in, or "out" for a fade-out effect. Default is `in`.

- **`start_frame, s`** Specify the number of the frame to start applying the fade effect at. Default is 0.

- **`nb_frames, n`** The number of frames that the fade effect lasts. At the end of the fade-in effect, the output video will have the same intensity as the input video. At the end of the fade-out transition, the output video will be filled with the selected `color`. Default is 25.

- **`alpha`** If set to 1, fade only alpha channel, if one exists on the input. Default value is 0.

- **`start_time, st`** Specify the timestamp (in seconds) of the frame to start to apply the fade effect. If both start_frame and start_time are specified, the fade will start at whichever comes last. Default is 0.

- **`duration, d`** The number of seconds for which the fade effect has to last. At the end of the fade-in effect the output video will have the same intensity as the input video, at the end of the fade-out transition the output video will be filled with the selected `color`. If both duration and nb_frames are specified, duration is used. Default is 0 (nb_frames is used by default).

- **`color, c`** Specify the color of the fade. Default is "black".

## Examples

- Fade in the first 30 frames of video:

  ``` text
  fade=in:0:30
  ```

  The command above is equivalent to:

  ``` text
  fade=t=in:s=0:n=30
  ```

- Fade out the last 45 frames of a 200-frame video:

  ``` text
  fade=out:155:45
  fade=type=out:start_frame=155:nb_frames=45
  ```

- Fade in the first 25 frames and fade out the last 25 frames of a 1000-frame video:

  ``` text
  fade=in:0:25, fade=out:975:25
  ```

- Make the first 5 frames yellow, then fade in from frame 5-24:

  ``` text
  fade=in:5:20:color=yellow
  ```

- Fade in alpha over first 25 frames of video:

  ``` text
  fade=in:0:25:alpha=1
  ```

- Make the first 5.5 seconds black, then fade in for 0.5 seconds:

  ``` text
  fade=t=in:st=5.5:d=0.5
  ```
