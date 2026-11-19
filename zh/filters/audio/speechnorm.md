# speechnorm

Speech Normalizer.

This filter expands or compresses each half-cycle of audio samples (local set of samples all above or all below zero and between two nearest zero crossings) depending on threshold value, so audio reaches target peak value under conditions controlled by below options.

The filter accepts the following options:

- **`peak, p`** Set the expansion target peak value. This specifies the highest allowed absolute amplitude level for the normalized audio input. Default value is 0.95. Allowed range is from 0.0 to 1.0.

- **`expansion, e`** Set the maximum expansion factor. Allowed range is from 1.0 to 50.0. Default value is 2.0. This option controls maximum local half-cycle of samples expansion. The maximum expansion would be such that local peak value reaches target peak value but never to surpass it and that ratio between new and previous peak value does not surpass this option value.

- **`compression, c`** Set the maximum compression factor. Allowed range is from 1.0 to 50.0. Default value is 2.0. This option controls maximum local half-cycle of samples compression. This option is used only if `threshold` option is set to value greater than 0.0, then in such cases when local peak is lower or same as value set by `threshold` all samples belonging to that peak's half-cycle will be compressed by current compression factor.

- **`threshold, t`** Set the threshold value. Default value is 0.0. Allowed range is from 0.0 to 1.0. This option specifies which half-cycles of samples will be compressed and which will be expanded. Any half-cycle samples with their local peak value below or same as this option value will be compressed by current compression factor, otherwise, if greater than threshold value they will be expanded with expansion factor so that it could reach peak target value but never surpass it.

- **`raise, r`** Set the expansion raising amount per each half-cycle of samples. Default value is 0.001. Allowed range is from 0.0 to 1.0. This controls how fast expansion factor is raised per each new half-cycle until it reaches `expansion` value. Setting this options too high may lead to distortions.

- **`fall, f`** Set the compression raising amount per each half-cycle of samples. Default value is 0.001. Allowed range is from 0.0 to 1.0. This controls how fast compression factor is raised per each new half-cycle until it reaches `compression` value.

- **`channels, h`** Specify which channels to filter, by default all available channels are filtered.

- **`invert, i`** Enable inverted filtering, by default is disabled. This inverts interpretation of `threshold` option. When enabled any half-cycle of samples with their local peak value below or same as `threshold` option will be expanded otherwise it will be compressed.

- **`link, l`** Link channels when calculating gain applied to each filtered channel sample, by default is disabled. When disabled each filtered channel gain calculation is independent, otherwise when this option is enabled the minimum of all possible gains for each filtered channel is used.

- **`rms, m`** Set the expansion target RMS value. This specifies the highest allowed RMS level for the normalized audio input. Default value is 0.0, thus disabled. Allowed range is from 0.0 to 1.0.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Weak and slow amplification:

  ``` text
  speechnorm=e=3:r=0.00001:l=1
  ```

- Moderate and slow amplification:

  ``` text
  speechnorm=e=6.25:r=0.00001:l=1
  ```

- Strong and fast amplification:

  ``` text
  speechnorm=e=12.5:r=0.0001:l=1
  ```

- Very strong and fast amplification:

  ``` text
  speechnorm=e=25:r=0.0001:l=1
  ```

- Extreme and fast amplification:

  ``` text
  speechnorm=e=50:r=0.0001:l=1
  ```
