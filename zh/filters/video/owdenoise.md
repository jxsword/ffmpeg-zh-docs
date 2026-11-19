# owdenoise

Apply Overcomplete Wavelet denoiser.

The filter accepts the following options:

- **`depth`** Set depth.

  Larger depth values will denoise lower frequency components more, but slow down filtering.

  Must be an int in the range 8-16, default is `8`.

- **`luma_strength, ls`** Set luma strength.

  Must be a double value in the range 0-1000, default is `1.0`.

- **`chroma_strength, cs`** Set chroma strength.

  Must be a double value in the range 0-1000, default is `1.0`.
