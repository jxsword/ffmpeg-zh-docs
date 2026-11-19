# colorspace_cuda

CUDA accelerated implementation of the colorspace filter.

It is by no means feature complete compared to the software colorspace filter, and at the current time only supports color range conversion between jpeg/full and mpeg/limited range.

The filter accepts the following options:

- **`range`** Specify output color range.

  The accepted values are:

  | Term     | Description             |
  |----------|-------------------------|
  | `tv`   | TV (restricted) range   |
  | `mpeg` | MPEG (restricted) range |
  | `pc`   | PC (full) range         |
  | `jpeg` | JPEG (full) range       |
