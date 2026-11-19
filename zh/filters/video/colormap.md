# colormap

Apply custom color maps to video stream.

This filter needs three input video streams. First stream is video stream that is going to be filtered out. Second and third video stream specify color patches for source color to target color mapping.

The filter accepts the following options:

- **`patch_size`** Set the source and target video stream patch size in pixels.

- **`nb_patches`** Set the max number of used patches from source and target video stream. Default value is number of patches available in additional video streams. Max allowed number of patches is `64`.

- **`type`** Set the adjustments used for target colors. Can be `relative` or `absolute`. Defaults is `absolute`.

- **`kernel`** Set the kernel used to measure color differences between mapped colors.

  The accepted values are:

  - **`euclidean`**

  - **`weuclidean`**

  Default is `euclidean`.
