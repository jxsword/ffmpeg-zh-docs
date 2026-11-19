# sofalizer

SOFAlizer uses head-related transfer functions (HRTFs) to create virtual loudspeakers around the user for binaural listening via headphones (audio formats up to 9 channels supported). The HRTFs are stored in SOFA files (see <http://www.sofacoustics.org/> for a database). SOFAlizer is developed at the Acoustics Research Institute (ARI) of the Austrian Academy of Sciences.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libmysofa`.

The filter accepts the following options:

- **`sofa`** Set the SOFA file used for rendering.

- **`gain`** Set gain applied to audio. Value is in dB. Default is 0.

- **`rotation`** Set rotation of virtual loudspeakers in deg. Default is 0.

- **`elevation`** Set elevation of virtual speakers in deg. Default is 0.

- **`radius`** Set distance in meters between loudspeakers and the listener with near-field HRTFs. Default is 1.

- **`type`** Set processing type. Can be \<time\> or \<freq\>. \<time\> is processing audio in time domain which is slow. \<freq\> is processing audio in frequency domain which is fast. Default is \<freq\>.

- **`speakers`** Set custom positions of virtual loudspeakers. Syntax for this option is: \<CH\> \<AZIM\> \<ELEV\>\[\|\<CH\> \<AZIM\> \<ELEV\>\|...\]. Each virtual loudspeaker is described with short channel name following with azimuth and elevation in degrees. Each virtual loudspeaker description is separated by '\|'. For example to override front left and front right channel positions use: 'speakers=FL 45 15\|FR 345 15'. Descriptions with unrecognised channel names are ignored.

- **`lfegain`** Set custom gain for LFE channels. Value is in dB. Default is 0.

- **`framesize`** Set custom frame size in number of samples. Default is 1024. Allowed range is from 1024 to 96000. Only used if option `type` is set to \<freq\>.

- **`normalize`** Should all IRs be normalized upon importing SOFA file. By default is enabled.

- **`interpolate`** Should nearest IRs be interpolated with neighbor IRs if exact position does not match. By default is disabled.

- **`minphase`** Minphase all IRs upon loading of SOFA file. By default is disabled.

- **`anglestep`** Set neighbor search angle step. Only used if option \<interpolate\> is enabled.

- **`radstep`** Set neighbor search radius step. Only used if option \<interpolate\> is enabled.

## Examples

- Using ClubFritz6 sofa file:

  ``` text
  sofalizer=sofa=/path/to/ClubFritz6.sofa:type=freq:radius=1
  ```

- Using ClubFritz12 sofa file and bigger radius with small rotation:

  ``` text
  sofalizer=sofa=/path/to/ClubFritz12.sofa:type=freq:radius=2:rotation=5
  ```

- Similar as above but with custom speaker positions for front left, front right, back left and back right and also with custom gain:

  ``` text
  "sofalizer=sofa=/path/to/ClubFritz6.sofa:type=freq:radius=2:speakers=FL 45|FR 315|BL 135|BR 225:gain=28"
  ```
