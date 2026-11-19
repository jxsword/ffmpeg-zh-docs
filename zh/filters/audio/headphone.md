# headphone

Apply head-related transfer functions (HRTFs) to create virtual loudspeakers around the user for binaural listening via headphones. The HRIRs are provided via additional streams, for each channel one stereo input stream is needed.

The filter accepts the following options:

- **`map`** Set mapping of input streams for convolution. The argument is a '\|'-separated list of channel names in order as they are given as additional stream inputs for filter. This also specify number of input streams. Number of input streams must be not less than number of channels in first stream plus one.

- **`gain`** Set gain applied to audio. Value is in dB. Default is 0.

- **`type`** Set processing type. Can be \<time\> or \<freq\>. \<time\> is processing audio in time domain which is slow. \<freq\> is processing audio in frequency domain which is fast. Default is \<freq\>.

- **`lfe`** Set custom gain for LFE channels. Value is in dB. Default is 0.

- **`size`** Set size of frame in number of samples which will be processed at once. Default value is \<1024\>. Allowed range is from 1024 to 96000.

- **`hrir`** Set format of hrir stream. Default value is \<stereo\>. Alternative value is \<multich\>. If value is set to \<stereo\>, number of additional streams should be greater or equal to number of input channels in first input stream. Also each additional stream should have stereo number of channels. If value is set to \<multich\>, number of additional streams should be exactly one. Also number of input channels of additional stream should be equal or greater than twice number of channels of first input stream.

## Examples

- Full example using wav files as coefficients with amovie filters for 7.1 downmix, each amovie filter use stereo file with IR coefficients as input. The files give coefficients for each position of virtual loudspeaker:

  ``` text
  ffmpeg -i input.wav
  -filter_complex "amovie=azi_270_ele_0_DFC.wav[sr];amovie=azi_90_ele_0_DFC.wav[sl];amovie=azi_225_ele_0_DFC.wav[br];amovie=azi_135_ele_0_DFC.wav[bl];amovie=azi_0_ele_0_DFC.wav,asplit[fc][lfe];amovie=azi_35_ele_0_DFC.wav[fl];amovie=azi_325_ele_0_DFC.wav[fr];[0:a][fl][fr][fc][lfe][bl][br][sl][sr]headphone=FL|FR|FC|LFE|BL|BR|SL|SR"
  output.wav
  ```

- Full example using wav files as coefficients with amovie filters for 7.1 downmix, but now in \<multich\> \<hrir\> format.

  ``` text
  ffmpeg -i input.wav -filter_complex "amovie=minp.wav[hrirs];[0:a][hrirs]headphone=map=FL|FR|FC|LFE|BL|BR|SL|SR:hrir=multich"
  output.wav
  ```
