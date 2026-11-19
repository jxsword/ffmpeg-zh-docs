# estdif

Deinterlace the input video ("estdif" stands for "Edge Slope Tracing Deinterlacing Filter").

Spatial only filter that uses edge slope tracing algorithm to interpolate missing lines. It accepts the following parameters:

- **`mode`** The interlacing mode to adopt. It accepts one of the following values:

  | Term    | Description                      |
  |---------|----------------------------------|
  | `frame` | Output one frame for each frame. |
  | `field` | Output one frame for each field. |

  The default value is `field`.

- **`parity`** The picture field parity assumed for the input interlaced video. It accepts one of the following values:

  | Term   | Description                                 |
  |--------|---------------------------------------------|
  | `tff`  | Assume the top field is first.              |
  | `bff`  | Assume the bottom field is first.           |
  | `auto` | Enable automatic detection of field parity. |

  The default value is `auto`. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.

- **`deint`** Specify which frames to deinterlace. Accepts one of the following values:

  | Term         | Description                                   |
  |--------------|-----------------------------------------------|
  | `all`        | Deinterlace all frames.                       |
  | `interlaced` | Only deinterlace frames marked as interlaced. |

  The default value is `all`.

- **`rslope`** Specify the search radius for edge slope tracing. Default value is 1. Allowed range is from 1 to 15.

- **`redge`** Specify the search radius for best edge matching. Default value is 2. Allowed range is from 0 to 15.

- **`ecost`** Specify the edge cost for edge matching. Default value is 2. Allowed range is from 0 to 50.

- **`mcost`** Specify the middle cost for edge matching. Default value is 1. Allowed range is from 0 to 50.

- **`dcost`** Specify the distance cost for edge matching. Default value is 1. Allowed range is from 0 to 50.

- **`interp`** Specify the interpolation used. Default is 4-point interpolation. It accepts one of the following values:

  | Term | Description               |
  |------|---------------------------|
  | `2p` | Two-point interpolation.  |
  | `4p` | Four-point interpolation. |
  | `6p` | Six-point interpolation.  |

## Commands

This filter supports same [commands](#commands) as options.
