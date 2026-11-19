# fftdnoiz

Denoise frames using 3D FFT (frequency domain filtering).

The filter accepts the following options:

- **`sigma`** Set the noise sigma constant. This sets denoising strength. Default value is 1. Allowed range is from 0 to 30. Using very high sigma with low overlap may give blocking artifacts.

- **`amount`** Set amount of denoising. By default all detected noise is reduced. Default value is 1. Allowed range is from 0 to 1.

- **`block`** Set size of block in pixels, Default is 32, can be 8 to 256.

- **`overlap`** Set block overlap. Default is 0.5. Allowed range is from 0.2 to 0.8.

- **`method`** Set denoising method. Default is `wiener`, can also be `hard`.

- **`prev`** Set number of previous frames to use for denoising. By default is set to 0.

- **`next`** Set number of next frames to to use for denoising. By default is set to 0.

- **`planes`** Set planes which will be filtered, by default are all available filtered except alpha.
