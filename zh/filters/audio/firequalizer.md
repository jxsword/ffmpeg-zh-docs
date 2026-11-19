# firequalizer

Apply FIR Equalization using arbitrary frequency response.

The filter accepts the following option:

- **`gain`** Set gain curve equation (in dB). The expression can contain variables:

  - **`f`** the evaluated frequency

  - **`sr`** sample rate

  - **`ch`** channel number, set to 0 when multichannels evaluation is disabled

  - **`chid`** channel id, see libavutil/channel_layout.h, set to the first channel id when multichannels evaluation is disabled

  - **`chs`** number of channels

  - **`chlayout`** channel_layout, see libavutil/channel_layout.h

  and functions:

  | Term | Description |
  |----|----|
  | `gain_interpolate(f)` | interpolate gain on frequency f based on gain_entry |
  | `cubic_interpolate(f)` | same as gain_interpolate, but smoother |

  This option is also available as command. Default is `gain_interpolate(f)`.

- **`gain_entry`** Set gain entry for gain_interpolate function. The expression can contain functions:

  | Term          | Description                                  |
  |---------------|----------------------------------------------|
  | `entry(f, g)` | store gain entry at frequency f with value g |

  This option is also available as command.

- **`delay`** Set filter delay in seconds. Higher value means more accurate. Default is `0.01`.

- **`accuracy`** Set filter accuracy in Hz. Lower value means more accurate. Default is `5`.

- **`wfunc`** Set window function. Acceptable values are:

  | Term | Description |
  |----|----|
  | `rectangular` | rectangular window, useful when gain curve is already smooth |
  | `hann` | hann window (default) |
  | `hamming` | hamming window |
  | `blackman` | blackman window |
  | `nuttall3` | 3-terms continuous 1st derivative nuttall window |
  | `mnuttall3` | minimum 3-terms discontinuous nuttall window |
  | `nuttall` | 4-terms continuous 1st derivative nuttall window |
  | `bnuttall` | minimum 4-terms discontinuous nuttall (blackman-nuttall) window |
  | `bharris` | blackman-harris window |
  | `tukey` | tukey window |

- **`fixed`** If enabled, use fixed number of audio samples. This improves speed when filtering with large delay. Default is disabled.

- **`multi`** Enable multichannels evaluation on gain. Default is disabled.

- **`zero_phase`** Enable zero phase mode by subtracting timestamp to compensate delay. Default is disabled.

- **`scale`** Set scale used by gain. Acceptable values are:

  | Term | Description |
  |----|----|
  | `linlin` | linear frequency, linear gain |
  | `linlog` | linear frequency, logarithmic (in dB) gain (default) |
  | `loglin` | logarithmic (in octave scale where 20 Hz is 0) frequency, linear gain |
  | `loglog` | logarithmic frequency, logarithmic gain |

- **`dumpfile`** Set file for dumping, suitable for gnuplot.

- **`dumpscale`** Set scale for dumpfile. Acceptable values are same with scale option. Default is linlog.

- **`fft2`** Enable 2-channel convolution using complex FFT. This improves speed significantly. Default is disabled.

- **`min_phase`** Enable minimum phase impulse response. Default is disabled.

## Examples

- lowpass at 1000 Hz:

  ``` text
  firequalizer=gain='if(lt(f,1000), 0, -INF)'
  ```

- lowpass at 1000 Hz with gain_entry:

  ``` c
  firequalizer=gain_entry='entry(1000,0); entry(1001, -INF)'
  ```

- custom equalization:

  ``` c
  firequalizer=gain_entry='entry(100,0); entry(400, -4); entry(1000, -6); entry(2000, 0)'
  ```

- higher delay with zero phase to compensate delay:

  ``` text
  firequalizer=delay=0.1:fixed=on:zero_phase=on
  ```

- lowpass on left channel, highpass on right channel:

  ``` c
  firequalizer=gain='if(eq(chid,1), gain_interpolate(f), if(eq(chid,2), gain_interpolate(1e6+f), 0))'
  :gain_entry='entry(1000, 0); entry(1001,-INF); entry(1e6+1000,0)':multi=on
  ```
