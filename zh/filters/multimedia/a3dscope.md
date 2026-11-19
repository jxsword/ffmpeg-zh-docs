# a3dscope

Convert input audio to 3d scope video output.

The filter accepts the following options:

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `hd720`.

- **`fov`** Set the camera field of view. Default is 90 degrees. Allowed range is from 40 to 150.

- **`roll`** Set the camera roll.

- **`pitch`** Set the camera pitch.

- **`yaw`** Set the camera yaw.

- **`xzoom`** Set the camera zoom on X-axis.

- **`yzoom`** Set the camera zoom on Y-axis.

- **`zzoom`** Set the camera zoom on Z-axis.

- **`xpos`** Set the camera position on X-axis.

- **`ypos`** Set the camera position on Y-axis.

- **`zpos`** Set the camera position on Z-axis.

- **`length`** Set the length of displayed audio waves in number of frames.

## Commands

Filter supports the some above options as [commands](#commands).
