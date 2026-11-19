# maskedclamp

Clamp the first input stream with the second input and third input stream.

Returns the value of first stream to be between second input stream - `undershoot` and third input stream + `overshoot`.

This filter accepts the following options:

- **`undershoot`** Default value is `0`.

- **`overshoot`** Default value is `0`.

- **`planes`** Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

## Commands

This filter supports the all above options as [commands](#commands).
