# colormatrix

Convert color matrix.

The filter accepts the following options:

- **`src`**

- **`dst`** Specify the source and destination color matrix. Both values must be specified.

  The accepted values are:

  | Term          | Description |
  |---------------|-------------|
  | `bt709`     | BT.709      |
  | `fcc`       | FCC         |
  | `bt601`     | BT.601      |
  | `bt470`     | BT.470      |
  | `bt470bg`   | BT.470BG    |
  | `smpte170m` | SMPTE-170M  |
  | `smpte240m` | SMPTE-240M  |
  | `bt2020`    | BT.2020     |

For example to convert from BT.601 to SMPTE-240M, use the command:

``` text
colormatrix=bt601:smpte240m
```
