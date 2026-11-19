# noise

Add noise on video input frame.

The filter accepts the following options:

- **`all_seed`**

- **`c0_seed`**

- **`c1_seed`**

- **`c2_seed`**

- **`c3_seed`** Set noise seed for specific pixel component or all pixel components in case of \<all_seed\>. Default value is `123457`.

- **`all_strength, alls`**

- **`c0_strength, c0s`**

- **`c1_strength, c1s`**

- **`c2_strength, c2s`**

- **`c3_strength, c3s`** Set noise strength for specific pixel component or all pixel components in case \<all_strength\>. Default value is `0`. Allowed range is \[0, 100\].

- **`all_flags, allf`**

- **`c0_flags, c0f`**

- **`c1_flags, c1f`**

- **`c2_flags, c2f`**

- **`c3_flags, c3f`** Set pixel component flags or set flags for all components if \<all_flags\>. Available values for component flags are:

  | Term  | Description                                           |
  |-------|-------------------------------------------------------|
  | `a` | averaged temporal noise (smoother)                    |
  | `p` | mix random noise with a (semi)regular pattern         |
  | `t` | temporal noise (noise pattern changes between frames) |
  | `u` | uniform noise (gaussian otherwise)                    |

## Examples

Add temporal and uniform noise to input video:

``` text
noise=alls=20:allf=t+u
```
