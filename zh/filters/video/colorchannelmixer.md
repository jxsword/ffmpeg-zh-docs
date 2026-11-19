# colorchannelmixer

Adjust video input frames by re-mixing color channels.

This filter modifies a color channel by adding the values associated to the other channels of the same pixels. For example if the value to modify is red, the output value will be:

``` text
red=red*rr + blue*rb + green*rg + alpha*ra
```

The filter accepts the following options:

- **`rr`**

- **`rg`**

- **`rb`**

- **`ra`** Adjust contribution of input red, green, blue and alpha channels for output red channel. Default is `1` for \<rr\>, and `0` for \<rg\>, \<rb\> and \<ra\>.

- **`gr`**

- **`gg`**

- **`gb`**

- **`ga`** Adjust contribution of input red, green, blue and alpha channels for output green channel. Default is `1` for \<gg\>, and `0` for \<gr\>, \<gb\> and \<ga\>.

- **`br`**

- **`bg`**

- **`bb`**

- **`ba`** Adjust contribution of input red, green, blue and alpha channels for output blue channel. Default is `1` for \<bb\>, and `0` for \<br\>, \<bg\> and \<ba\>.

- **`ar`**

- **`ag`**

- **`ab`**

- **`aa`** Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is `1` for \<aa\>, and `0` for \<ar\>, \<ag\> and \<ab\>.

  Allowed ranges for options are `[-2.0, 2.0]`.

- **`pc`** Set preserve color mode. The accepted values are:

  | Term     | Description                                |
  |----------|--------------------------------------------|
  | `none` | Disable color preserving, this is default. |
  | `lum`  | Preserve luminance.                        |
  | `max`  | Preserve max value of RGB triplet.         |
  | `avg`  | Preserve average value of RGB triplet.     |
  | `sum`  | Preserve sum value of RGB triplet.         |
  | `nrm`  | Preserve normalized value of RGB triplet.  |
  | `pwr`  | Preserve power value of RGB triplet.       |

- **`pa`** Set the preserve color amount when changing colors. Allowed range is from `[0.0, 1.0]`. Default is `0.0`, thus disabled.

## Examples

- Convert source to grayscale:

  ``` text
  colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3
  ```

- Simulate sepia tones:

  ``` text
  colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131
  ```

## Commands

This filter supports the all above options as [commands](#commands).
