# nlmeans_vulkan

Denoise frames using Non-Local Means algorithm, implemented on the GPU using Vulkan. Supports more pixel formats than [nlmeans](nlmeans.md#nlmeans) or [nlmeans_opencl](../overview.md#example), including alpha channel support.

The filter accepts the following options.

- **`s`** Set denoising strength for all components. Default is 1.0. Must be in range \[0.0, 100.0\].

- **`p`** Set patch size for all planes. Default is 7. Must be odd number in range \[0, 99\].

- **`r`** Set research size. Default is 15. Must be odd number in range \[0, 99\].

- **`t`** Set parallelism. Default is 8. Must be a number in the range \[1, 64\]. Larger values will use more VRAM but may not result in greater speed. The optimal value is hardware and input dependent.

- **`s0`**

- **`s1`**

- **`s2`**

- **`s3`** Set denoising strength for a specific component. Default is \<1.0\>, equal to `s`. Must be in range \[0.0, 100.0\]. 0.0 disables denoising in that component.

- **`p0`**

- **`p1`**

- **`p2`**

- **`p3`** Set patch size for a specific component. Default is \<7\>, equal to `p`. Must be odd number in range \[0, 99\].
