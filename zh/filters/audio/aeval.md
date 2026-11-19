# aeval

Modify an audio signal according to the specified expressions.

This filter accepts one or more expressions (one for each channel), which are evaluated and used to modify a corresponding audio signal.

It accepts the following parameters:

- **`exprs`** Set the '\|'-separated expressions list for each separate channel. If the number of input channels is greater than the number of expressions, the last specified expression is used for the remaining output channels.

- **`channel_layout, c`** Set output channel layout. If not specified, the channel layout is specified by the number of expressions. If set to `same`, it will use by default the same input channel layout.

Each expression in \<exprs\> can contain the following constants and functions:

- **`ch`** channel number of the current expression

- **`n`** number of the evaluated sample, starting from 0

- **`s`** sample rate

- **`t`** time of the evaluated sample expressed in seconds

- **`nb_in_channels`**

- **`nb_out_channels`** input and output number of channels

- **`val(CH)`** the value of input channel with number \<CH\>

Note: this filter is slow. For faster processing you should use a dedicated filter.

## Examples

- Half volume:

  ``` text
  aeval=val(ch)/2:c=same
  ```

- Invert phase of the second channel:

  ``` text
  aeval=val(0)|-val(1)
  ```
