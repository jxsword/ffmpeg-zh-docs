# volume

Adjust the input audio volume.

It accepts the following parameters:

- **`volume`** Set audio volume expression.

  Output values are clipped to the maximum value.

  The output audio volume is given by the relation:

  ``` text
  output_volume = volume * input_volume
  ```

  The default value for \<volume\> is "1.0".

- **`precision`** This parameter represents the mathematical precision.

  It determines which input sample formats will be allowed, which affects the precision of the volume scaling.

  | Term | Description |
  |----|----|
  | `fixed` | 8-bit fixed-point; this limits input sample format to U8, S16, and S32. |
  | `float` | 32-bit floating-point; this limits input sample format to FLT. (default) |
  | `double` | 64-bit floating-point; this limits input sample format to DBL. |

- **`replaygain`** Choose the behaviour on encountering ReplayGain side data in input frames.

  | Term | Description |
  |----|----|
  | `drop` | Remove ReplayGain side data, ignoring its contents (the default). |
  | `ignore` | Ignore ReplayGain side data, but leave it in the frame. |
  | `track` | Prefer the track gain, if present. |
  | `album` | Prefer the album gain, if present. |

- **`replaygain_preamp`** Pre-amplification gain in dB to apply to the selected replaygain gain.

  Default value for \<replaygain_preamp\> is 0.0.

- **`replaygain_noclip`** Prevent clipping by limiting the gain applied.

  Default value for \<replaygain_noclip\> is 1.

- **`eval`** Set when the volume expression is evaluated.

  It accepts the following values:

  - **`once`** only evaluate expression once during the filter initialization, or when the `volume` command is sent

  - **`frame`** evaluate expression for each incoming frame

  Default value is `once`.

The volume expression can contain the following parameters.

| Term | Description |
|----|----|
| `n` | frame number (starting at zero) |
| `nb_channels` | number of channels |
| `nb_consumed_samples` | number of samples consumed by the filter |
| `nb_samples` | number of samples in the current frame |
| `pos` | original frame position in the file; deprecated, do not use |
| `pts` | frame PTS |
| `sample_rate` | sample rate |
| `startpts` | PTS at start of stream |
| `startt` | time at start of stream |
| `t` | frame time |
| `tb` | timestamp timebase |
| `volume` | last set volume value |

Note that when `eval` is set to `once` only the \<sample_rate\> and \<tb\> variables are available, all other variables will evaluate to NAN.

## Commands

This filter supports the following commands:

- **`volume`** Modify the volume expression. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.

## Examples

- Halve the input audio volume:

  ``` text
  volume=volume=0.5
  volume=volume=1/2
  volume=volume=-6.0206dB
  ```

  In all the above example the named key for `volume` can be omitted, for example like in:

  ``` text
  volume=0.5
  ```

- Increase input audio power by 6 decibels using fixed-point precision:

  ``` text
  volume=volume=6dB:precision=fixed
  ```

- Fade volume after time 10 with an annihilation period of 5 seconds:

  ``` text
  volume='if(lt(t,10),1,max(1-(t-10)/5,0))':eval=frame
  ```
