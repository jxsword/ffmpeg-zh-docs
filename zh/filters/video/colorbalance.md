# colorbalance

Modify intensity of primary colors (red, green and blue) of input frames.

The filter allows an input frame to be adjusted in the shadows, midtones or highlights regions for the red-cyan, green-magenta or blue-yellow balance.

A positive adjustment value shifts the balance towards the primary color, a negative value towards the complementary color.

The filter accepts the following options:

- **`rs`**

- **`gs`**

- **`bs`** Adjust red, green and blue shadows (darkest pixels).

- **`rm`**

- **`gm`**

- **`bm`** Adjust red, green and blue midtones (medium pixels).

- **`rh`**

- **`gh`**

- **`bh`** Adjust red, green and blue highlights (brightest pixels).

  Allowed ranges for options are `[-1.0, 1.0]`. Defaults are `0`.

- **`pl`** Preserve lightness when changing color balance. Default is disabled.

## Examples

- Add red color cast to shadows:

  ``` text
  colorbalance=rs=.3
  ```

## Commands

This filter supports the all above options as [commands](#commands).
