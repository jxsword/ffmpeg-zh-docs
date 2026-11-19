# bwdif_cuda

Deinterlace the input video using the [bwdif](bwdif.md#bwdif) algorithm, but implemented in CUDA so that it can work as part of a GPU accelerated pipeline with nvdec and/or nvenc.

It accepts the following parameters:

- **`mode`** The interlacing mode to adopt. It accepts one of the following values:

  | Term            | Description                      |
  |-----------------|----------------------------------|
  | `0, send_frame` | Output one frame for each frame. |
  | `1, send_field` | Output one frame for each field. |

  The default value is `send_field`.

- **`parity`** The picture field parity assumed for the input interlaced video. It accepts one of the following values:

  | Term       | Description                                 |
  |------------|---------------------------------------------|
  | `0, tff`   | Assume the top field is first.              |
  | `1, bff`   | Assume the bottom field is first.           |
  | `-1, auto` | Enable automatic detection of field parity. |

  The default value is `auto`. If the interlacing is unknown or the decoder does not export this information, top field first will be assumed.

- **`deint`** Specify which frames to deinterlace. Accepts one of the following values:

  | Term            | Description                                   |
  |-----------------|-----------------------------------------------|
  | `0, all`        | Deinterlace all frames.                       |
  | `1, interlaced` | Only deinterlace frames marked as interlaced. |

  The default value is `all`.
