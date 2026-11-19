# mestimate

Estimate and export motion vectors using block matching algorithms. Motion vectors are stored in frame side data to be used by other filters.

This filter accepts the following options:

- **`method`** Specify the motion estimation method. Accepts one of the following values:

  | Term      | Description                                   |
  |-----------|-----------------------------------------------|
  | `esa`   | Exhaustive search algorithm.                  |
  | `tss`   | Three step search algorithm.                  |
  | `tdls`  | Two dimensional logarithmic search algorithm. |
  | `ntss`  | New three step search algorithm.              |
  | `fss`   | Four step search algorithm.                   |
  | `ds`    | Diamond search algorithm.                     |
  | `hexbs` | Hexagon-based search algorithm.               |
  | `epzs`  | Enhanced predictive zonal search algorithm.   |
  | `umh`   | Uneven multi-hexagon search algorithm.        |

  Default value is `esa`.

- **`mb_size`** Macroblock size. Default `16`.

- **`search_param`** Search parameter. Default `7`.
