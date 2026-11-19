# codecview

Visualize information exported by some codecs.

Some codecs can export information through frames using side-data or other means. For example, some MPEG based codecs export motion vectors through the \<export_mvs\> flag in the codec `flags2` option.

The filter accepts the following option:

- **`block`** Display block partition structure using the luma plane.

- **`mv`** Set motion vectors to visualize.

  Available flags for \<mv\> are:

  | Term   | Description                        |
  |--------|------------------------------------|
  | `pf` | forward predicted MVs of P-frames  |
  | `bf` | forward predicted MVs of B-frames  |
  | `bb` | backward predicted MVs of B-frames |

- **`qp`** Display quantization parameters using the chroma planes.

- **`mv_type, mvt`** Set motion vectors type to visualize. Includes MVs from all frames unless specified by \<frame_type\> option.

  Available flags for \<mv_type\> are:

  | Term   | Description            |
  |--------|------------------------|
  | `fp` | forward predicted MVs  |
  | `bp` | backward predicted MVs |

- **`frame_type, ft`** Set frame type to visualize motion vectors of.

  Available flags for \<frame_type\> are:

  | Term   | Description                                  |
  |--------|----------------------------------------------|
  | `if` | intra-coded frames (I-frames)                |
  | `pf` | predicted frames (P-frames)                  |
  | `bf` | bi-directionally predicted frames (B-frames) |

## Examples

- Visualize forward predicted MVs of all frames using `ffplay`:

  ``` text
  ffplay -flags2 +export_mvs input.mp4 -vf codecview=mv_type=fp
  ```

- Visualize multi-directionals MVs of P and B-Frames using `ffplay`:

  ``` text
  ffplay -flags2 +export_mvs input.mp4 -vf codecview=mv=pf+bf+bb
  ```
