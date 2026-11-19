# colorhold

Remove all color information for all RGB colors except for certain one.

The filter accepts the following options:

- **`color`** The color which will not be replaced with neutral gray.

- **`similarity`** Similarity percentage with the above color. 0.01 matches only the exact key color, while 1.0 matches everything.

- **`blend`** Blend percentage. 0.0 makes pixels fully gray. Higher values result in more preserved color.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
