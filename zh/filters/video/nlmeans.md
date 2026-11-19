# nlmeans

Denoise frames using Non-Local Means algorithm.

Each pixel is adjusted by looking for other pixels with similar contexts. This context similarity is defined by comparing their surrounding patches of size `p`x`p`. Patches are searched in an area of `r`x`r` around the pixel.

Note that the research area defines centers for patches, which means some patches will be made of pixels outside that research area.

The filter accepts the following options.

- **`s`** Set denoising strength. Default is 1.0. Must be in range \[1.0, 30.0\].

- **`p`** Set patch size. Default is 7. Must be odd number in range \[0, 99\].

- **`pc`** Same as `p` but for chroma planes.

  The default value is \<0\> and means automatic.

- **`r`** Set research size. Default is 15. Must be odd number in range \[0, 99\].

- **`rc`** Same as `r` but for chroma planes.

  The default value is \<0\> and means automatic.
