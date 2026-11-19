# xstack_vaapi

Stack video inputs into custom layout.

This is the VA-API variant of the [xstack](xstack.md#xstack) filter, each input stream may have different size, this filter will scale down/up each input stream to the given output size, or the size of the first input stream.

It accepts the following options:

- **`inputs`** See [xstack](xstack.md#xstack).

- **`shortest`** See [xstack](xstack.md#xstack).

- **`layout`** See [xstack](xstack.md#xstack). Moreover, this permits the user to supply output size for each input stream.

  ``` text
  xstack_vaapi=inputs=4:layout=0_0_1920x1080|0_h0_1920x1080|w0_0_1920x1080|w0_h0_1920x1080
  ```

- **`grid`** See [xstack](xstack.md#xstack).

- **`grid_tile_size`** Set output size for each input stream when `grid` is set. If this option is not set, this filter will set output size by default to the size of the first input stream. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`fill`** See [xstack](xstack.md#xstack).
