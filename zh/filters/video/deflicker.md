# deflicker

Remove temporal frame luminance variations.

It accepts the following options:

- **`size, s`** Set moving-average filter size in frames. Default is 5. Allowed range is 2 - 129.

- **`mode, m`** Set averaging mode to smooth temporal luminance variations.

  Available values are:

  | Term       | Description     |
  |------------|-----------------|
  | `am`     | Arithmetic mean |
  | `gm`     | Geometric mean  |
  | `hm`     | Harmonic mean   |
  | `qm`     | Quadratic mean  |
  | `cm`     | Cubic mean      |
  | `pm`     | Power mean      |
  | `median` | Median          |

- **`bypass`** Do not actually modify frame. Useful when one only wants metadata.
