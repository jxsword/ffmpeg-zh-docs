# setpts, asetpts

Change the PTS (presentation timestamp) of the input frames.

`setpts` works on video frames, `asetpts` on audio frames.

This filter accepts the following options:

- **`expr`** The expression which is evaluated for each frame to construct its timestamp.

- **`strip_fps (video only)`** Boolean option which determines if the original framerate and frame duration metadata is unset. If set to true, be advised that a sane frame rate should be explicitly specified if output is sent to a constant frame rate muxer. Default is `false`.

The expression is evaluated through the eval API and can contain the following constants:

- **`FRAME_RATE, FR`** frame rate, only defined for constant frame-rate video

- **`PTS`** The presentation timestamp in input

- **`N`** The count of the input frame for video or the number of consumed samples, not including the current frame for audio, starting from 0.

- **`NB_CONSUMED_SAMPLES`** The number of consumed samples, not including the current frame (only audio)

- **`NB_SAMPLES, S`** The number of samples in the current frame (only audio)

- **`SAMPLE_RATE, SR`** The audio sample rate.

- **`STARTPTS`** The PTS of the first frame.

- **`STARTT`** the time in seconds of the first frame

- **`INTERLACED`** State whether the current frame is interlaced.

- **`T`** the time in seconds of the current frame

- **`POS`** original position in the file of the frame, or undefined if undefined for the current frame; deprecated, do not use

- **`PREV_INPTS`** The previous input PTS.

- **`PREV_INT`** previous input time in seconds

- **`PREV_OUTPTS`** The previous output PTS.

- **`PREV_OUTT`** previous output time in seconds

- **`RTCTIME`** The wallclock (RTC) time in microseconds. This is deprecated, use time(0) instead.

- **`RTCSTART`** The wallclock (RTC) time at the start of the movie in microseconds.

- **`TB`** The timebase of the input timestamps.

- **`T_CHANGE`** Time of the first frame after command was applied or time of the first frame if no commands.

## Examples

- Start counting PTS from zero

  ``` text
  setpts=PTS-STARTPTS
  ```

- Apply fast motion effect:

  ``` text
  setpts=0.5*PTS
  ```

- Apply slow motion effect:

  ``` text
  setpts=2.0*PTS
  ```

- Set fixed rate of 25 frames per second:

  ``` text
  setpts=N/(25*TB)
  ```

- Apply a random jitter effect of +/-100 TB units:

  ``` text
  setpts=PTS+randomi(0, -100\,100)
  ```

- Set fixed rate 25 fps with some jitter:

  ``` text
  setpts='1/(25*TB) * (N + 0.05 * sin(N*2*PI/25))'
  ```

- Apply an offset of 10 seconds to the input PTS:

  ``` text
  setpts=PTS+10/TB
  ```

- Generate timestamps from a "live source" and rebase onto the current timebase:

  ``` text
  setpts='(RTCTIME - RTCSTART) / (TB * 1000000)'
  ```

- Generate timestamps by counting samples:

  ``` text
  asetpts=N/SR/TB
  ```

## Commands

Both filters support all above options as [commands](#commands).
