# surround

Apply audio surround upmix filter.

This filter allows to produce multichannel output from audio stream.

The filter accepts the following options:

- **`chl_out`** Set output channel layout. By default, this is \<5.1\>.

  See section "the Channel Layout section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the required syntax.

- **`chl_in`** Set input channel layout. By default, this is \<stereo\>.

  See section "the Channel Layout section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the required syntax.

- **`level_in`** Set input volume level. By default, this is \<1\>.

- **`level_out`** Set output volume level. By default, this is \<1\>.

- **`lfe`** Enable LFE channel output if output channel layout has it. By default, this is enabled.

- **`lfe_low`** Set LFE low cut off frequency. By default, this is \<128\> Hz.

- **`lfe_high`** Set LFE high cut off frequency. By default, this is \<256\> Hz.

- **`lfe_mode`** Set LFE mode, can be \<add\> or \<sub\>. Default is \<add\>. In \<add\> mode, LFE channel is created from input audio and added to output. In \<sub\> mode, LFE channel is created from input audio and added to output but also all non-LFE output channels are subtracted with output LFE channel.

- **`smooth`** Set temporal smoothness strength, used to gradually change factors when transforming stereo sound in time. Allowed range is from \<0.0\> to \<1.0\>. Useful to improve output quality with \<focus\> option values greater than \<0.0\>. Default is \<0.0\>. Only values inside this range and without edges are effective.

- **`angle`** Set angle of stereo surround transform, Allowed range is from \<0\> to \<360\>. Default is \<90\>.

- **`focus`** Set focus of stereo surround transform, Allowed range is from \<-1\> to \<1\>. Default is \<0\>.

- **`fc_in`** Set front center input volume. By default, this is \<1\>.

- **`fc_out`** Set front center output volume. By default, this is \<1\>.

- **`fl_in`** Set front left input volume. By default, this is \<1\>.

- **`fl_out`** Set front left output volume. By default, this is \<1\>.

- **`fr_in`** Set front right input volume. By default, this is \<1\>.

- **`fr_out`** Set front right output volume. By default, this is \<1\>.

- **`sl_in`** Set side left input volume. By default, this is \<1\>.

- **`sl_out`** Set side left output volume. By default, this is \<1\>.

- **`sr_in`** Set side right input volume. By default, this is \<1\>.

- **`sr_out`** Set side right output volume. By default, this is \<1\>.

- **`bl_in`** Set back left input volume. By default, this is \<1\>.

- **`bl_out`** Set back left output volume. By default, this is \<1\>.

- **`br_in`** Set back right input volume. By default, this is \<1\>.

- **`br_out`** Set back right output volume. By default, this is \<1\>.

- **`bc_in`** Set back center input volume. By default, this is \<1\>.

- **`bc_out`** Set back center output volume. By default, this is \<1\>.

- **`lfe_in`** Set LFE input volume. By default, this is \<1\>.

- **`lfe_out`** Set LFE output volume. By default, this is \<1\>.

- **`allx`** Set spread usage of stereo image across X axis for all channels. Allowed range is from \<-1\> to \<15\>. By default this value is negative \<-1\>, and thus unused.

- **`ally`** Set spread usage of stereo image across Y axis for all channels. Allowed range is from \<-1\> to \<15\>. By default this value is negative \<-1\>, and thus unused.

- **`fcx, flx, frx, blx, brx, slx, srx, bcx`** Set spread usage of stereo image across X axis for each channel. Allowed range is from \<0.06\> to \<15\>. By default this value is \<0.5\>.

- **`fcy, fly, fry, bly, bry, sly, sry, bcy`** Set spread usage of stereo image across Y axis for each channel. Allowed range is from \<0.06\> to \<15\>. By default this value is \<0.5\>.

- **`win_size`** Set window size. Allowed range is from \<1024\> to \<65536\>. Default size is \<4096\>.

- **`win_func`** Set window function.

  It accepts the following values:

  - **`rect`**

  - **`bartlett`**

  - **`hann, hanning`**

  - **`hamming`**

  - **`blackman`**

  - **`welch`**

  - **`flattop`**

  - **`bharris`**

  - **`bnuttall`**

  - **`bhann`**

  - **`sine`**

  - **`nuttall`**

  - **`lanczos`**

  - **`gauss`**

  - **`tukey`**

  - **`dolph`**

  - **`cauchy`**

  - **`parzen`**

  - **`poisson`**

  - **`bohman`**

  - **`kaiser`**

  Default is `hann`.

- **`overlap`** Set window overlap. If set to 1, the recommended overlap for selected window function will be picked. Default is `0.5`.
