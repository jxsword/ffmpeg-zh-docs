# sab

Apply Shape Adaptive Blur.

The filter accepts the following options:

- **`luma_radius, lr`** Set luma blur filter strength, must be a value in range 0.1-4.0, default value is 1.0. A greater value will result in a more blurred image, and in slower processing.

- **`luma_pre_filter_radius, lpfr`** Set luma pre-filter radius, must be a value in the 0.1-2.0 range, default value is 1.0.

- **`luma_strength, ls`** Set luma maximum difference between pixels to still be considered, must be a value in the 0.1-100.0 range, default value is 1.0.

- **`chroma_radius, cr`** Set chroma blur filter strength, must be a value in range -0.9-4.0. A greater value will result in a more blurred image, and in slower processing.

- **`chroma_pre_filter_radius, cpfr`** Set chroma pre-filter radius, must be a value in the -0.9-2.0 range.

- **`chroma_strength, cs`** Set chroma maximum difference between pixels to still be considered, must be a value in the -0.9-100.0 range.

Each chroma option value, if not explicitly specified, is set to the corresponding luma option value.
