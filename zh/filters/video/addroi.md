# addroi

Mark a region of interest in a video frame.

The frame data is passed through unchanged, but metadata is attached to the frame indicating regions of interest which can affect the behaviour of later encoding. Multiple regions can be marked by applying the filter multiple times.

- **`x`** Region distance in pixels from the left edge of the frame.

- **`y`** Region distance in pixels from the top edge of the frame.

- **`w`** Region width in pixels.

- **`h`** Region height in pixels.

  The parameters \<x\>, \<y\>, \<w\> and \<h\> are expressions, and may contain the following variables:

  | Term | Description                |
  |------|----------------------------|
  | `iw` | Width of the input frame.  |
  | `ih` | Height of the input frame. |

- **`qoffset`** Quantisation offset to apply within the region.

  This must be a real value in the range -1 to +1. A value of zero indicates no quality change. A negative value asks for better quality (less quantisation), while a positive value asks for worse quality (greater quantisation).

  The range is calibrated so that the extreme values indicate the largest possible offset - if the rest of the frame is encoded with the worst possible quality, an offset of -1 indicates that this region should be encoded with the best possible quality anyway. Intermediate values are then interpolated in some codec-dependent way.

  For example, in 10-bit H.264 the quantisation parameter varies between -12 and 51. A typical qoffset value of -1/10 therefore indicates that this region should be encoded with a QP around one-tenth of the full range better than the rest of the frame. So, if most of the frame were to be encoded with a QP of around 30, this region would get a QP of around 24 (an offset of approximately -1/10 \* (51 - -12) = -6.3). An extreme value of -1 would indicate that this region should be encoded with the best possible quality regardless of the treatment of the rest of the frame - that is, should be encoded at a QP of -12.

- **`clear`** If set to true, remove any existing regions of interest marked on the frame before adding the new one.

## Examples

- Mark the centre quarter of the frame as interesting.

  ``` text
  addroi=iw/4:ih/4:iw/2:ih/2:-1/10
  ```

- Mark the 100-pixel-wide region on the left edge of the frame as very uninteresting (to be encoded at much lower quality than the rest of the frame).

  ``` text
  addroi=0:0:100:ih:+1/5
  ```
