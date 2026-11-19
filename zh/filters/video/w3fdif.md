# w3fdif

Deinterlace the input video ("w3fdif" stands for "Weston 3 Field Deinterlacing Filter").

Based on the process described by Martin Weston for BBC R&D, and implemented based on the de-interlace algorithm written by Jim Easterbrook for BBC R&D, the Weston 3 field deinterlacing filter uses filter coefficients calculated by BBC R&D.

This filter uses field-dominance information in frame to decide which of each pair of fields to place first in the output. If it gets it wrong use [setfield](setfield.md#setfield) filter before `w3fdif` filter.

There are two sets of filter coefficients, so called "simple" and "complex". Which set of filter coefficients is used can be set by passing an optional parameter:

- **`filter`** Set the interlacing filter coefficients. Accepts one of the following values:

  | Term        | Description                          |
  |-------------|--------------------------------------|
  | `simple`  | Simple filter coefficient set.       |
  | `complex` | More-complex filter coefficient set. |

  Default value is `complex`.

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

  | Term           | Description                                   |
  |----------------|-----------------------------------------------|
  | `all`        | Deinterlace all frames,                       |
  | `interlaced` | Only deinterlace frames marked as interlaced. |

  Default value is `all`.

## Commands

This filter supports same [commands](#commands) as options.
