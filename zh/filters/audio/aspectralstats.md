# aspectralstats

Display frequency domain statistical information about the audio channels. Statistics are calculated and stored as metadata for each audio channel and for each audio frame.

It accepts the following option:

- **`win_size`** Set the window length in samples. Default value is 2048. Allowed range is from 32 to 65536.

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

- **`overlap`** Set window overlap. Allowed range is from `0` to `1`. Default value is `0.5`.

- **`measure`** Select the parameters which are measured. The metadata keys can be used as flags, default is `all` which measures everything. `none` disables all measurement.

A list of each metadata key follows:

- **`mean`**

- **`variance`**

- **`centroid`**

- **`spread`**

- **`skewness`**

- **`kurtosis`**

- **`entropy`**

- **`flatness`**

- **`crest`**

- **`flux`**

- **`slope`**

- **`decrease`**

- **`rolloff`**
