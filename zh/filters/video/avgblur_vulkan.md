# avgblur_vulkan

Apply an average blur filter, implemented on the GPU using Vulkan.

The filter accepts the following options:

- **`sizeX`** Set horizontal radius size. Range is `[1, 32]` and default value is `3`.

- **`sizeY`** Set vertical radius size. Range is `[1, 32]` and default value is `3`.

- **`planes`** Set which planes to filter. Default value is `0xf`, by which all planes are processed.
