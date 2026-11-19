# limitdiff

Apply limited difference filter using second and optionally third video stream.

The filter accepts the following options:

- **`threshold`** Set the threshold to use when allowing certain differences between video streams. Any absolute difference value lower or exact than this threshold will pick pixel components from first video stream.

- **`elasticity`** Set the elasticity of soft thresholding when processing video streams. This value multiplied with first one sets second threshold. Any absolute difference value greater or exact than second threshold will pick pixel components from second video stream. For values between those two threshold linear interpolation between first and second video stream will be used.

- **`reference`** Enable the reference (third) video stream processing. By default is disabled. If set, this video stream will be used for calculating absolute difference with first video stream.

- **`planes`** Specify which planes will be processed. Defaults to all available.

## Commands

This filter supports the all above options as [commands](#commands) except option `reference`.
