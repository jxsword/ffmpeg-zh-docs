# extractplanes

Extract color channel components from input video stream into separate grayscale video streams.

The filter accepts the following option:

- **`planes`** Set plane(s) to extract.

  Available values for planes are:

  - **`y`**

  - **`u`**

  - **`v`**

  - **`a`**

  - **`r`**

  - **`g`**

  - **`b`**

  Choosing planes not available in the input will result in an error. That means you cannot select `r`, `g`, `b` planes with `y`, `u`, `v` planes at same time.

## Examples

- Extract luma, u and v color channel component from input video frame into 3 grayscale outputs:

  ``` text
  ffmpeg -i video.avi -filter_complex 'extractplanes=y+u+v[y][u][v]' -map '[y]' y.avi -map '[u]' u.avi -map '[v]' v.avi
  ```
