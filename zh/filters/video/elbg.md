# elbg

Apply a posterize effect using the ELBG (Enhanced LBG) algorithm.

For each input image, the filter will compute the optimal mapping from the input to the output given the codebook length, that is the number of distinct output colors.

This filter accepts the following options.

- **`codebook_length, l`** Set codebook length. The value must be a positive integer, and represents the number of distinct output colors. Default value is 256.

- **`nb_steps, n`** Set the maximum number of iterations to apply for computing the optimal mapping. The higher the value the better the result and the higher the computation time. Default value is 1.

- **`seed, s`** Set a random seed, must be an integer included between 0 and UINT32_MAX. If not specified, or if explicitly set to -1, the filter will try to use a good random seed on a best effort basis.

- **`pal8`** Set pal8 output pixel format. This option does not work with codebook length greater than 256. Default is disabled.

- **`use_alpha`** Include alpha values in the quantization calculation. Allows creating palettized output images (e.g. PNG8) with multiple alpha smooth blending.
