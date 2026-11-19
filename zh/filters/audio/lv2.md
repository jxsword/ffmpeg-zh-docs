# lv2

Load a LV2 (LADSPA Version 2) plugin.

To enable compilation of this filter you need to configure FFmpeg with `--enable-lv2`.

- **`plugin, p`** Specifies the plugin URI. You may need to escape ':'.

- **`controls, c`** Set the '\|' separated list of controls which are zero or more floating point values that determine the behavior of the loaded plugin (for example delay, threshold or gain). If `controls` is set to `help`, all available controls and their valid ranges are printed.

- **`sample_rate, s`** Specify the sample rate, default to 44100. Only used if plugin have zero inputs.

- **`nb_samples, n`** Set the number of samples per channel per each output frame, default is 1024. Only used if plugin have zero inputs.

- **`duration, d`** Set the minimum duration of the sourced audio. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax. Note that the resulting duration may be greater than the specified duration, as the generated audio is always cut at the end of a complete frame. If not specified, or the expressed duration is negative, the audio is supposed to be generated forever. Only used if plugin have zero inputs.

## Examples

- Apply bass enhancer plugin from Calf:

  ``` text
  lv2=p=http\\\\://calf.sourceforge.net/plugins/BassEnhancer:c=amount=2
  ```

- Apply vinyl plugin from Calf:

  ``` text
  lv2=p=http\\\\://calf.sourceforge.net/plugins/Vinyl:c=drone=0.2|aging=0.5
  ```

- Apply bit crusher plugin from ArtyFX:

  ``` text
  lv2=p=http\\\\://www.openavproductions.com/artyfx#bitta:c=crush=0.3
  ```

## Commands

This filter supports all options that are exported by plugin as commands.
