# colorcontrast

Adjust color contrast between RGB components.

The filter accepts the following options:

- **`rc`** Set the red-cyan contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.

- **`gm`** Set the green-magenta contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.

- **`by`** Set the blue-yellow contrast. Defaults is 0.0. Allowed range is from -1.0 to 1.0.

- **`rcw`**

- **`gmw`**

- **`byw`** Set the weight of each `rc`, `gm`, `by` option value. Default value is 0.0. Allowed range is from 0.0 to 1.0. If all weights are 0.0 filtering is disabled.

- **`pl`** Set the amount of preserving lightness. Default value is 0.0. Allowed range is from 0.0 to 1.0.

## Commands

This filter supports the all above options as [commands](#commands).
