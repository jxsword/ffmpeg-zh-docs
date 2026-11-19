# perms, aperms

Set read/write permissions for the output frames.

These filters are mainly aimed at developers to test direct path in the following filter in the filtergraph.

The filters accept the following options:

- **`mode`** Select the permissions mode.

  It accepts the following values:

  | Term | Description |
  |----|----|
  | `none` | Do nothing. This is the default. |
  | `ro` | Set all the output frames read-only. |
  | `rw` | Set all the output frames directly writable. |
  | `toggle` | Make the frame read-only if writable, and writable if read-only. |
  | `random` | Set each output frame read-only or writable randomly. |

- **`seed`** Set the seed for the \<random\> mode, must be an integer included between `0` and `UINT32_MAX`. If not specified, or if explicitly set to `-1`, the filter will try to use a good random seed on a best effort basis.

Note: in case of auto-inserted filter between the permission filter and the following one, the permission might not be received as expected in that following filter. Inserting a [format](../video/format.md#format) or [aformat](../audio/aformat.md#aformat) filter before the perms/aperms filter can avoid this problem.
