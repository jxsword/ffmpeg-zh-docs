# astats

Display time domain statistical information about the audio channels. Statistics are calculated and displayed for each audio channel and, where applicable, an overall figure is also given.

It accepts the following option:

- **`length`** Short window length in seconds, used for peak and through RMS measurement. Default is `0.05` (50 milliseconds). Allowed range is `[0 - 10]`.

- **`metadata`** Set metadata injection. All the metadata keys are prefixed with `lavfi.astats.X`, where `X` is channel number starting from 1 or string `Overall`. Default is disabled.

  Available keys for each channel are: \<Bit_depth\> \<Crest_factor\> \<DC_offset\> \<Dynamic_range\> \<Entropy\> \<Flat_factor\> \<Max_difference\> \<Max_level\> \<Mean_difference\> \<Min_difference\> \<Min_level\> \<Noise_floor\> \<Noise_floor_count\> \<Number_of_Infs\> \<Number_of_NaNs\> \<Number_of_denormals\> \<Peak_count\> \<Abs_Peak_count\> \<Peak_level\> \<RMS_difference\> \<RMS_peak\> \<RMS_trough\> \<Zero_crossings\> \<Zero_crossings_rate\>

  and for `Overall`: \<Bit_depth\> \<DC_offset\> \<Entropy\> \<Flat_factor\> \<Max_difference\> \<Max_level\> \<Mean_difference\> \<Min_difference\> \<Min_level\> \<Noise_floor\> \<Noise_floor_count\> \<Number_of_Infs\> \<Number_of_NaNs\> \<Number_of_denormals\> \<Number_of_samples\> \<Peak_count\> \<Abs_Peak_count\> \<Peak_level\> \<RMS_difference\> \<RMS_level\> \<RMS_peak\> \<RMS_trough\>

  For example, a full key looks like `lavfi.astats.1.DC_offset` or `lavfi.astats.Overall.Peak_count`.

  Read below for the description of the keys.

- **`reset`** Set the number of frames over which cumulative stats are calculated before being reset. Default is disabled.

- **`measure_perchannel`** Select the parameters which are measured per channel. The metadata keys can be used as flags, default is `all` which measures everything. `none` disables all per channel measurement.

- **`measure_overall`** Select the parameters which are measured overall. The metadata keys can be used as flags, default is `all` which measures everything. `none` disables all overall measurement.

A description of the measure keys follow:

- **`none`** no measures

- **`all`** all measures

- **`Bit_depth`** overall bit depth of audio, i.e. number of bits used for each sample

- **`Crest_factor`** standard ratio of peak to RMS level (note: not in dB)

- **`DC_offset`** mean amplitude displacement from zero

- **`Dynamic_range`** measured dynamic range of audio in dB

- **`Entropy`** entropy measured across whole audio, entropy of value near 1.0 is typically measured for white noise

- **`Flat_factor`** flatness (i.e. consecutive samples with the same value) of the signal at its peak levels (i.e. either \<Min_level\> or \<Max_level\>)

- **`Max_difference`** maximal difference between two consecutive samples

- **`Max_level`** maximal sample level

- **`Mean_difference`** mean difference between two consecutive samples, i.e. the average of each difference between two consecutive samples

- **`Min_difference`** minimal difference between two consecutive samples

- **`Min_level`** minimal sample level

- **`Noise_floor`** minimum local peak measured in dBFS over a short window

- **`Noise_floor_count`** number of occasions (not the number of samples) that the signal attained \<Noise floor\>

- **`Number_of_Infs`** number of samples with an infinite value

- **`Number_of_NaNs`** number of samples with a NaN (not a number) value

- **`Number_of_denormals`** number of samples with a subnormal value

- **`Number_of_samples`** number of samples

- **`Peak_count`** number of occasions (not the number of samples) that the signal attained either \<Min_level\> or \<Max_level\>

- **`Abs_Peak_count`** number of occasions that the absolute samples taken from the signal attained max absolute value of \<Min_level\> and \<Max_level\>

- **`Peak_level`** standard peak level measured in dBFS

- **`RMS_difference`** Root Mean Square difference between two consecutive samples

- **`RMS_level`** standard RMS level measured in dBFS

- **`RMS_peak`**

- **`RMS_trough`** peak and through values for RMS level measured over a short window, measured in dBFS.

- **`Zero crossings`** number of points where the waveform crosses the zero level axis

- **`Zero crossings rate`** rate of Zero crossings and number of audio samples
