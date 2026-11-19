# spectrumsynth

Synthesize audio from 2 input video spectrums, first input stream represents magnitude across time and second represents phase across time. The filter will transform from frequency domain as displayed in videos back to time domain as presented in audio output.

This filter is primarily created for reversing processed [showspectrum](showspectrum.md#showspectrum) filter outputs, but can synthesize sound from other spectrograms too. But in such case results are going to be poor if the phase data is not available, because in such cases phase data need to be recreated, usually it's just recreated from random noise. For best results use gray only output (`channel` color mode in [showspectrum](showspectrum.md#showspectrum) filter) and `log` scale for magnitude video and `lin` scale for phase video. To produce phase, for 2nd video, use `data` option. Inputs videos should generally use `fullframe` slide mode as that saves resources needed for decoding video.

The filter accepts the following options:

- **`sample_rate`** Specify sample rate of output audio, the sample rate of audio from which spectrum was generated may differ.

- **`channels`** Set number of channels represented in input video spectrums.

- **`scale`** Set scale which was used when generating magnitude input spectrum. Can be `lin` or `log`. Default is `log`.

- **`slide`** Set slide which was used when generating inputs spectrums. Can be `replace`, `scroll`, `fullframe` or `rscroll`. Default is `fullframe`.

- **`win_func`** Set window function used for resynthesis.

- **`overlap`** Set window overlap. In range `[0, 1]`. Default is `1`, which means optimal overlap for selected window function will be picked.

- **`orientation`** Set orientation of input videos. Can be `vertical` or `horizontal`. Default is `vertical`.

## Examples

- First create magnitude and phase videos from audio, assuming audio is stereo with 44100 sample rate, then resynthesize videos back to audio with spectrumsynth:

  ``` text
  ffmpeg -i input.flac -lavfi showspectrum=mode=separate:scale=log:overlap=0.875:color=channel:slide=fullframe:data=magnitude -an -c:v rawvideo magnitude.nut
  ffmpeg -i input.flac -lavfi showspectrum=mode=separate:scale=lin:overlap=0.875:color=channel:slide=fullframe:data=phase -an -c:v rawvideo phase.nut
  ffmpeg -i magnitude.nut -i phase.nut -lavfi spectrumsynth=channels=2:sample_rate=44100:win_func=hann:overlap=0.875:slide=fullframe output.flac
  ```
