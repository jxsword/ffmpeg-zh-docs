# il

Deinterleave or interleave fields.

This filter allows one to process interlaced images fields without deinterlacing them. Deinterleaving splits the input frame into 2 fields (so called half pictures). Odd lines are moved to the top half of the output image, even lines to the bottom half. You can process (filter) them independently and then re-interleave them.

The filter accepts the following options:

- **`luma_mode, l`**

- **`chroma_mode, c`**

- **`alpha_mode, a`** Available values for \<luma_mode\>, \<chroma_mode\> and \<alpha_mode\> are:

  | Term | Description |
  |----|----|
  | `none` | Do nothing. |
  | `deinterleave, d` | Deinterleave fields, placing one above the other. |
  | `interleave, i` | Interleave fields. Reverse the effect of deinterleaving. |

  Default value is `none`.

- **`luma_swap, ls`**

- **`chroma_swap, cs`**

- **`alpha_swap, as`** Swap luma/chroma/alpha fields. Exchange even & odd lines. Default value is `0`.

## Commands

This filter supports the all above options as [commands](#commands).
