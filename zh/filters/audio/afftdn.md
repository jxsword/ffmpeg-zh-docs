# afftdn

Denoise audio samples with FFT.

A description of the accepted parameters follows.

- **`noise_reduction, nr`** Set the noise reduction in dB, allowed range is 0.01 to 97. Default value is 12 dB.

- **`noise_floor, nf`** Set the noise floor in dB, allowed range is -80 to -20. Default value is -50 dB.

- **`noise_type, nt`** Set the noise type.

  It accepts the following values:

  - **`white, w`** Select white noise.

  - **`vinyl, v`** Select vinyl noise.

  - **`shellac, s`** Select shellac noise.

  - **`custom, c`** Select custom noise, defined in `bn` option.

    Default value is white noise.

- **`band_noise, bn`** Set custom band noise profile for every one of 15 bands. Bands are separated by ' ' or '\|'.

- **`residual_floor, rf`** Set the residual floor in dB, allowed range is -80 to -20. Default value is -38 dB.

- **`track_noise, tn`** Enable noise floor tracking. By default is disabled. With this enabled, noise floor is automatically adjusted.

- **`track_residual, tr`** Enable residual tracking. By default is disabled.

- **`output_mode, om`** Set the output mode.

  It accepts the following values:

  - **`input, i`** Pass input unchanged.

  - **`output, o`** Pass noise filtered out.

  - **`noise, n`** Pass only noise.

    Default value is \<output\>.

- **`adaptivity, ad`** Set the adaptivity factor, used how fast to adapt gains adjustments per each frequency bin. Value \<0\> enables instant adaptation, while higher values react much slower. Allowed range is from \<0\> to \<1\>. Default value is \<0.5\>.

- **`floor_offset, fo`** Set the noise floor offset factor. This option is used to adjust offset applied to measured noise floor. It is only effective when noise floor tracking is enabled. Allowed range is from \<-2.0\> to \<2.0\>. Default value is \<1.0\>.

- **`noise_link, nl`** Set the noise link used for multichannel audio.

  It accepts the following values:

  - **`none`** Use unchanged channel's noise floor.

  - **`min`** Use measured min noise floor of all channels.

  - **`max`** Use measured max noise floor of all channels.

  - **`average`** Use measured average noise floor of all channels.

    Default value is \<min\>.

- **`band_multiplier, bm`** Set the band multiplier factor, used how much to spread bands across frequency bins. Allowed range is from \<0.2\> to \<5\>. Default value is \<1.25\>.

- **`sample_noise, sn`** Toggle capturing and measurement of noise profile from input audio.

  It accepts the following values:

  - **`start, begin`** Start sample noise capture.

  - **`stop, end`** Stop sample noise capture and measure new noise band profile.

    Default value is `none`.

- **`gain_smooth, gs`** Set gain smooth spatial radius, used to smooth gains applied to each frequency bin. Useful to reduce random music noise artefacts. Higher values increases smoothing of gains. Allowed range is from `0` to `50`. Default value is `0`.

## Commands

This filter supports the some above mentioned options as [commands](#commands).

## Examples

- Reduce white noise by 10dB, and use previously measured noise floor of -40dB:

  ``` text
  afftdn=nr=10:nf=-40
  ```

- Reduce white noise by 10dB, also set initial noise floor to -80dB and enable automatic tracking of noise floor so noise floor will gradually change during processing:

  ``` text
  afftdn=nr=10:nf=-80:tn=1
  ```

- Reduce noise by 20dB, using noise floor of -40dB and using commands to take noise profile of first 0.4 seconds of input audio:

  ``` text
  asendcmd=0.0 afftdn sn start,asendcmd=0.4 afftdn sn stop,afftdn=nr=20:nf=-40
  ```
