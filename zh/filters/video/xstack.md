# xstack

Stack video inputs into custom layout.

All streams must be of same pixel format.

The filter accepts the following options:

- **`inputs`** Set number of input streams. Default is 2.

- **`layout`** Specify layout of inputs. This option requires the desired layout configuration to be explicitly set by the user. This sets position of each video input in output. Each input is separated by '\|'. The first number represents the column, and the second number represents the row. Numbers start at 0 and are separated by '\_'. Optionally one can use wX and hX, where X is video input from which to take width or height. Multiple values can be used when separated by '+'. In such case values are summed together.

  Note that if inputs are of different sizes gaps may appear, as not all of the output video frame will be filled. Similarly, videos can overlap each other if their position doesn't leave enough space for the full frame of adjoining videos.

  For 2 inputs, a default layout of `0_0|w0_0` (equivalent to `grid=2x1`) is set. In all other cases, a layout or a grid must be set by the user. Either `grid` or `layout` can be specified at a time. Specifying both will result in an error.

- **`grid`** Specify a fixed size grid of inputs. This option is used to create a fixed size grid of the input streams. Set the grid size in the form `COLUMNSxROWS`. There must be `ROWS * COLUMNS` input streams and they will be arranged as a grid with `ROWS` rows and `COLUMNS` columns. When using this option, each input stream within a row must have the same height and all the rows must have the same width.

  If `grid` is set, then `inputs` option is ignored and is implicitly set to `ROWS * COLUMNS`.

  For 2 inputs, a default grid of `2x1` (equivalent to `layout=0_0|w0_0`) is set. In all other cases, a layout or a grid must be set by the user. Either `grid` or `layout` can be specified at a time. Specifying both will result in an error.

- **`shortest`** If set to 1, force the output to terminate when the shortest input terminates. Default value is 0.

- **`fill`** If set to valid color, all unused pixels will be filled with that color. By default fill is set to none, so it is disabled.

## Examples

- Display 4 inputs into 2x2 grid.

  Layout:

  ``` text
  input1(0, 0)  | input3(w0, 0)
  input2(0, h0) | input4(w0, h0)
  ```

  ``` text
  xstack=inputs=4:layout=0_0|0_h0|w0_0|w0_h0
  ```

  Note that if inputs are of different sizes, gaps or overlaps may occur.

- Display 4 inputs into 1x4 grid.

  Layout:

  ``` text
  input1(0, 0)
  input2(0, h0)
  input3(0, h0+h1)
  input4(0, h0+h1+h2)
  ```

  ``` text
  xstack=inputs=4:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2
  ```

  Note that if inputs are of different widths, unused space will appear.

- Display 9 inputs into 3x3 grid.

  Layout:

  ``` text
  input1(0, 0)       | input4(w0, 0)      | input7(w0+w3, 0)
  input2(0, h0)      | input5(w0, h0)     | input8(w0+w3, h0)
  input3(0, h0+h1)   | input6(w0, h0+h1)  | input9(w0+w3, h0+h1)
  ```

  ``` text
  xstack=inputs=9:layout=0_0|0_h0|0_h0+h1|w0_0|w0_h0|w0_h0+h1|w0+w3_0|w0+w3_h0|w0+w3_h0+h1
  ```

  Note that if inputs are of different sizes, gaps or overlaps may occur.

- Display 16 inputs into 4x4 grid.

  Layout:

  ``` text
  input1(0, 0)       | input5(w0, 0)       | input9 (w0+w4, 0)       | input13(w0+w4+w8, 0)
  input2(0, h0)      | input6(w0, h0)      | input10(w0+w4, h0)      | input14(w0+w4+w8, h0)
  input3(0, h0+h1)   | input7(w0, h0+h1)   | input11(w0+w4, h0+h1)   | input15(w0+w4+w8, h0+h1)
  input4(0, h0+h1+h2)| input8(w0, h0+h1+h2)| input12(w0+w4, h0+h1+h2)| input16(w0+w4+w8, h0+h1+h2)
  ```

  ``` text
  xstack=inputs=16:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2|w0_0|w0_h0|w0_h0+h1|w0_h0+h1+h2|w0+w4_0|
  w0+w4_h0|w0+w4_h0+h1|w0+w4_h0+h1+h2|w0+w4+w8_0|w0+w4+w8_h0|w0+w4+w8_h0+h1|w0+w4+w8_h0+h1+h2
  ```

  Note that if inputs are of different sizes, gaps or overlaps may occur.
