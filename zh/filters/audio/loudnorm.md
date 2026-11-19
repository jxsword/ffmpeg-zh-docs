# loudnorm

EBU R128 loudness normalization. Includes both dynamic and linear normalization modes. Support for both single pass (livestreams, files) and double pass (files) modes. This algorithm can target IL, LRA, and maximum true peak. In dynamic mode, to accurately detect true peaks, the audio stream will be upsampled to 192 kHz. Use the `-ar` option or `aresample` filter to explicitly set an output sample rate.

The filter accepts the following options:

- **`I, i`** Set integrated loudness target. Range is -70.0 - -5.0. Default value is -24.0.

- **`LRA, lra`** Set loudness range target. Range is 1.0 - 50.0. Default value is 7.0.

- **`TP, tp`** Set maximum true peak. Range is -9.0 - +0.0. Default value is -2.0.

- **`measured_I, measured_i`** Measured IL of input file. Range is -99.0 - +0.0.

- **`measured_LRA, measured_lra`** Measured LRA of input file. Range is 0.0 - 99.0.

- **`measured_TP, measured_tp`** Measured true peak of input file. Range is -99.0 - +99.0.

- **`measured_thresh`** Measured threshold of input file. Range is -99.0 - +0.0.

- **`offset`** Set offset gain. Gain is applied before the true-peak limiter. Range is -99.0 - +99.0. Default is +0.0.

- **`linear`** Normalize by linearly scaling the source audio. `measured_I`, `measured_LRA`, `measured_TP`, and `measured_thresh` must all be specified. Target LRA shouldn't be lower than source LRA and the change in integrated loudness shouldn't result in a true peak which exceeds the target TP. If any of these conditions aren't met, normalization mode will revert to \<dynamic\>. Options are `true` or `false`. Default is `true`.

- **`dual_mono`** Treat mono input files as "dual-mono". If a mono file is intended for playback on a stereo system, its EBU R128 measurement will be perceptually incorrect. If set to `true`, this option will compensate for this effect. Multi-channel input files are not affected by this option. Options are true or false. Default is false.

- **`print_format`** Set print format for stats. Options are summary, json, or none. Default value is none.

- **`stats_file`** Write stats to specified file. Format is controlled by `print_format`, which must be set. Specify `-` to write to standard output. Default is unset.
