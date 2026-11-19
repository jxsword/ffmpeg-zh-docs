# ladspa

Load a LADSPA (Linux Audio Developer's Simple Plugin API) plugin.

To enable compilation of this filter you need to configure FFmpeg with `--enable-ladspa`.

- **`file, f`** Specifies the name of LADSPA plugin library to load. If the environment variable `LADSPA_PATH` is defined, the LADSPA plugin is searched in each one of the directories specified by the colon separated list in `LADSPA_PATH`, otherwise in the standard LADSPA paths, which are in this order: `HOME/.ladspa/lib/`, `/usr/local/lib/ladspa/`, `/usr/lib/ladspa/`.

- **`plugin, p`** Specifies the plugin within the library. Some libraries contain only one plugin, but others contain many of them. If this is not set filter will list all available plugins within the specified library.

- **`controls, c`** Set the '\|' separated list of controls which are zero or more floating point values that determine the behavior of the loaded plugin (for example delay, threshold or gain). Controls need to be defined using the following syntax: c0=\<value0\>\|c1=\<value1\>\|c2=\<value2\>\|..., where \<valuei\> is the value set on the \<i\>-th control. Alternatively they can be also defined using the following syntax: \<value0\>\|\<value1\>\|\<value2\>\|..., where \<valuei\> is the value set on the \<i\>-th control. If `controls` is set to `help`, all available controls and their valid ranges are printed.

- **`sample_rate, s`** Specify the sample rate, default to 44100. Only used if plugin have zero inputs.

- **`nb_samples, n`** Set the number of samples per channel per each output frame, default is 1024. Only used if plugin have zero inputs.

- **`duration, d`** Set the minimum duration of the sourced audio. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. Note that the resulting duration may be greater than the specified duration, as the generated audio is always cut at the end of a complete frame. If not specified, or the expressed duration is negative, the audio is supposed to be generated forever. Only used if plugin have zero inputs.

- **`latency, l`** Enable latency compensation, by default is disabled. Only used if plugin have inputs.

## Examples

- List all available plugins within amp (LADSPA example plugin) library:

  ``` text
  ladspa=file=amp
  ```

- List all available controls and their valid ranges for `vcf_notch` plugin from `VCF` library:

  ``` text
  ladspa=f=vcf:p=vcf_notch:c=help
  ```

- Simulate low quality audio equipment using `Computer Music Toolkit` (CMT) plugin library:

  ``` text
  ladspa=file=cmt:plugin=lofi:controls=c0=22|c1=12|c2=12
  ```

- Add reverberation to the audio using TAP-plugins (Tom's Audio Processing plugins):

  ``` text
  ladspa=file=tap_reverb:tap_reverb
  ```

- Generate white noise, with 0.2 amplitude:

  ``` text
  ladspa=file=cmt:noise_source_white:c=c0=.2
  ```

- Generate 20 bpm clicks using plugin `C* Click - Metronome` from the `C* Audio Plugin Suite` (CAPS) library:

  ``` text
  ladspa=file=caps:Click:c=c1=20'
  ```

- Apply `C* Eq10X2 - Stereo 10-band equaliser` effect:

  ``` text
  ladspa=caps:Eq10X2:c=c0=-48|c9=-24|c3=12|c4=2
  ```

- Increase volume by 20dB using fast lookahead limiter from Steve Harris `SWH Plugins` collection:

  ``` text
  ladspa=fast_lookahead_limiter_1913:fastLookaheadLimiter:20|0|2
  ```

- Attenuate low frequencies using Multiband EQ from Steve Harris `SWH Plugins` collection:

  ``` text
  ladspa=mbeq_1197:mbeq:-24|-24|-24|0|0|0|0|0|0|0|0|0|0|0|0
  ```

- Reduce stereo image using `Narrower` from the `C* Audio Plugin Suite` (CAPS) library:

  ``` text
  ladspa=caps:Narrower
  ```

- Another white noise, now using `C* Audio Plugin Suite` (CAPS) library:

  ``` text
  ladspa=caps:White:.2
  ```

- Some fractal noise, using `C* Audio Plugin Suite` (CAPS) library:

  ``` text
  ladspa=caps:Fractal:c=c1=1
  ```

- Dynamic volume normalization using `VLevel` plugin:

  ``` text
  ladspa=vlevel-ladspa:vlevel_mono
  ```

## Commands

This filter supports the following commands:

- **`cN`** Modify the \<N\>-th control value.

  If the specified value is not valid, it is ignored and prior one is kept.
