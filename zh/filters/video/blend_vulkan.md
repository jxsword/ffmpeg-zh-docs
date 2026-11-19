# blend_vulkan

Blend two Vulkan frames into each other.

The `blend` filter takes two input streams and outputs one stream, the first input is the "top" layer and second input is "bottom" layer. By default, the output terminates when the longest input terminates.

A description of the accepted options follows.

- **`c0_mode`**

- **`c1_mode`**

- **`c2_mode`**

- **`c3_mode`**

- **`all_mode`** Set blend mode for specific pixel component or all pixel components in case of \<all_mode\>. Default value is `normal`.

  Available values for component modes are:

  - **`normal`**

  - **`multiply`**
