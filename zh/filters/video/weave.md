# weave, doubleweave

The `weave` takes a field-based video input and join each two sequential fields into single frame, producing a new double height clip with half the frame rate and half the frame count.

The `doubleweave` works same as `weave` but without halving frame rate and frame count.

It accepts the following option:

- **`first_field`** Set first field. Available values are:

  | Term          | Description                          |
  |---------------|--------------------------------------|
  | `top, t`    | Set the frame as top-field-first.    |
  | `bottom, b` | Set the frame as bottom-field-first. |

## Examples

- Interlace video using [select](../overview.md#examples) and [separatefields](separatefields.md#separatefields) filter:

  ``` text
  separatefields,select=eq(mod(n,4),0)+eq(mod(n,4),3),weave
  ```
