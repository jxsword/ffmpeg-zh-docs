# afwtdn

Reduce broadband noise from input samples using Wavelets.

A description of the accepted options follows.

- **`sigma`** Set the noise sigma, allowed range is from 0 to 1. Default value is 0. This option controls strength of denoising applied to input samples. Most useful way to set this option is via decibels, eg. -45dB.

- **`levels`** Set the number of wavelet levels of decomposition. Allowed range is from 1 to 12. Default value is 10. Setting this too low make denoising performance very poor.

- **`wavet`** Set wavelet type for decomposition of input frame. They are sorted by number of coefficients, from lowest to highest. More coefficients means worse filtering speed, but overall better quality. Available wavelets are:

  - **`sym2`**

  - **`sym4`**

  - **`rbior68`**

  - **`deb10`**

  - **`sym10`**

  - **`coif5`**

  - **`bl3`**

- **`percent`** Set percent of full denoising. Allowed range is from 0 to 100 percent. Default value is 85 percent or partial denoising.

- **`profile`** If enabled, first input frame will be used as noise profile. If first frame samples contain non-noise performance will be very poor.

- **`adaptive`** If enabled, input frames are analyzed for presence of noise. If noise is detected with high possibility then input frame profile will be used for processing following frames, until new noise frame is detected.

- **`samples`** Set size of single frame in number of samples. Allowed range is from 512 to 65536. Default frame size is 8192 samples.

- **`softness`** Set softness applied inside thresholding function. Allowed range is from 0 to 10. Default softness is 1.

## Commands

This filter supports the all above options as [commands](#commands).
