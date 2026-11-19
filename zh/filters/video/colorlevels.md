# colorlevels

Adjust video input frames using levels.

The filter accepts the following options:

- **`rimin`**

- **`gimin`**

- **`bimin`**

- **`aimin`** Adjust red, green, blue and alpha input black point. Allowed ranges for options are `[-1.0, 1.0]`. Defaults are `0`.

- **`rimax`**

- **`gimax`**

- **`bimax`**

- **`aimax`** Adjust red, green, blue and alpha input white point. Allowed ranges for options are `[-1.0, 1.0]`. Defaults are `1`.

  Input levels are used to lighten highlights (bright tones), darken shadows (dark tones), change the balance of bright and dark tones.

- **`romin`**

- **`gomin`**

- **`bomin`**

- **`aomin`** Adjust red, green, blue and alpha output black point. Allowed ranges for options are `[0, 1.0]`. Defaults are `0`.

- **`romax`**

- **`gomax`**

- **`bomax`**

- **`aomax`** Adjust red, green, blue and alpha output white point. Allowed ranges for options are `[0, 1.0]`. Defaults are `1`.

  Output levels allows manual selection of a constrained output level range.

- **`preserve`** Set preserve color mode. The accepted values are:

  | Term     | Description                                |
  |----------|--------------------------------------------|
  | `none` | Disable color preserving, this is default. |
  | `lum`  | Preserve luminance.                        |
  | `max`  | Preserve max value of RGB triplet.         |
  | `avg`  | Preserve average value of RGB triplet.     |
  | `sum`  | Preserve sum value of RGB triplet.         |
  | `nrm`  | Preserve normalized value of RGB triplet.  |
  | `pwr`  | Preserve power value of RGB triplet.       |

## Examples

- Make video output darker:

  ``` text
  colorlevels=rimin=0.058:gimin=0.058:bimin=0.058
  ```

- Increase contrast:

  ``` text
  colorlevels=rimin=0.039:gimin=0.039:bimin=0.039:rimax=0.96:gimax=0.96:bimax=0.96
  ```

- Make video output lighter:

  ``` text
  colorlevels=rimax=0.902:gimax=0.902:bimax=0.902
  ```

- Increase brightness:

  ``` text
  colorlevels=romin=0.5:gomin=0.5:bomin=0.5
  ```

## Commands

This filter supports the all above options as [commands](#commands).
