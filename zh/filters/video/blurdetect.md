# blurdetect

Determines blurriness of frames without altering the input frames.

Based on Marziliano, Pina, et al. "A no-reference perceptual blur metric." Allows for a block-based abbreviation.

The filter accepts the following options:

- **`low`**

- **`high`** Set low and high threshold values used by the Canny thresholding algorithm.

  The high threshold selects the "strong" edge pixels, which are then connected through 8-connectivity with the "weak" edge pixels selected by the low threshold.

  \<low\> and \<high\> threshold values must be chosen in the range \[0,1\], and \<low\> should be lesser or equal to \<high\>.

  Default value for \<low\> is `20/255`, and default value for \<high\> is `50/255`.

- **`radius`** Define the radius to search around an edge pixel for local maxima.

- **`block_pct`** Determine blurriness only for the most significant blocks, given in percentage.

- **`block_width`** Determine blurriness for blocks of width \<block_width\>. If set to any value smaller 1, no blocks are used and the whole image is processed as one no matter of \<block_height\>.

- **`block_height`** Determine blurriness for blocks of height \<block_height\>. If set to any value smaller 1, no blocks are used and the whole image is processed as one no matter of \<block_width\>.

- **`planes`** Set planes to filter. Default is first only.

## Examples

- Determine blur for 80% of most significant 32x32 blocks:

  ``` text
  blurdetect=block_width=32:block_height=32:block_pct=80
  ```
