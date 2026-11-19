# bm3d

Denoise frames using Block-Matching 3D algorithm.

The filter accepts the following options.

- **`sigma`** Set denoising strength. Default value is 1. Allowed range is from 0 to 999.9. The denoising algorithm is very sensitive to sigma, so adjust it according to the source.

- **`block`** Set local patch size. This sets dimensions in 2D.

- **`bstep`** Set sliding step for processing blocks. Default value is 4. Allowed range is from 1 to 64. Smaller values allows processing more reference blocks and is slower.

- **`group`** Set maximal number of similar blocks for 3rd dimension. Default value is 1. When set to 1, no block matching is done. Larger values allows more blocks in single group. Allowed range is from 1 to 256.

- **`range`** Set radius for search block matching. Default is 9. Allowed range is from 1 to INT32_MAX.

- **`mstep`** Set step between two search locations for block matching. Default is 1. Allowed range is from 1 to 64. Smaller is slower.

- **`thmse`** Set threshold of mean square error for block matching. Valid range is 0 to INT32_MAX.

- **`hdthr`** Set thresholding parameter for hard thresholding in 3D transformed domain. Larger values results in stronger hard-thresholding filtering in frequency domain.

- **`estim`** Set filtering estimation mode. Can be `basic` or `final`. Default is `basic`.

- **`ref`** If enabled, filter will use 2nd stream for block matching. Default is disabled for `basic` value of \<estim\> option, and always enabled if value of \<estim\> is `final`.

- **`planes`** Set planes to filter. Default is all available except alpha.

## Examples

- Basic filtering with bm3d:

  ``` text
  bm3d=sigma=3:block=4:bstep=2:group=1:estim=basic
  ```

- Same as above, but filtering only luma:

  ``` text
  bm3d=sigma=3:block=4:bstep=2:group=1:estim=basic:planes=1
  ```

- Same as above, but with both estimation modes:

  ``` text
  split[a][b],[a]bm3d=sigma=3:block=4:bstep=2:group=1:estim=basic[a],[b][a]bm3d=sigma=3:block=4:bstep=2:group=16:estim=final:ref=1
  ```

- Same as above, but prefilter with [nlmeans](nlmeans.md#nlmeans) filter instead:

  ``` text
  split[a][b],[a]nlmeans=s=3:r=7:p=3[a],[b][a]bm3d=sigma=3:block=4:bstep=2:group=16:estim=final:ref=1
  ```
