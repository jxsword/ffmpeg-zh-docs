# morpho

This filter allows to apply main morphological grayscale transforms, erode and dilate with arbitrary structures set in second input stream.

Unlike naive implementation and much slower performance in [erosion](erosion.md#erosion) and [dilation](dilation.md#dilation) filters, when speed is critical `morpho` filter should be used instead.

A description of accepted options follows,

- **`mode`** Set morphological transform to apply, can be:

  - **`erode`**

  - **`dilate`**

  - **`open`**

  - **`close`**

  - **`gradient`**

  - **`tophat`**

  - **`blackhat`**

  Default is `erode`.

- **`planes`** Set planes to filter, by default all planes except alpha are filtered.

- **`structure`** Set which structure video frames will be processed from second input stream, can be \<first\> or \<all\>. Default is \<all\>.

The `morpho` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Commands

This filter supports same [commands](#commands) as options.
